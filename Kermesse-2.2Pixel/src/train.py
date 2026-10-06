"""
Entrenamiento de Kermesse.   Uso (desde la carpeta src/):
    python train.py                      # entrenamiento completo por defecto
    python train.py --steps 35000 --lr 2e-3
    python train.py --resume             # continúa desde checkpoints/kermesse_21pixel

Cómo se usa el dataset (importante):
  * Cada ejemplo es una conversación completa; el agrupamiento por longitud limita el consumo de memoria.
  * La pérdida se calcula sobre lo que dice Kermesse (peso 1.0) y apenas sobre lo que dice la persona (0.1):
    el modelo gasta su capacidad en aprender a RESPONDER, no a imitar al usuario.
  * Las conversaciones se agrupan por largo para casi no desperdiciar cómputo en relleno (padding).
  * Se mide la pérdida en un set de validación que el modelo NUNCA ve entrenando.
"""
import argparse
import gc
import json
import os
import time
import numpy as np

import engine
from engine import cross_entropy, no_grad
from tokenizer import CharTokenizer, parse_dialogues, encode_conversation
from kermesse_model import KermesseModel
from optimizer import AdamW, lr_at
from checkpoint import save_model, load_model, load_opt_state

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CKPT = os.path.join(ROOT, "checkpoints", "kermesse_21pixel")
MODEL_NAME = "Kermesse-2.1Pixel"
MAX_PARAMS = 2_000_000


def load_split(path, tok, user_weight):
    convs = parse_dialogues(open(path, encoding="utf-8").read())
    return [encode_conversation(tok, c, user_weight) for c in convs]


def make_batches(examples, token_budget, rng, max_bs=64):
    idx = rng.permutation(len(examples))
    batches = []
    chunk = 1500
    for s in range(0, len(idx), chunk):
        grp = sorted(idx[s:s + chunk], key=lambda i: len(examples[i][0]))
        cur = []
        for i in grp:
            L = len(examples[i][0])
            if cur and (len(cur) + 1) * L > token_budget or len(cur) >= max_bs:
                batches.append(cur); cur = []
            cur.append(i)
        if cur:
            batches.append(cur)
    rng.shuffle(batches)
    return batches


def collate(examples, ids):
    L = max(len(examples[i][0]) for i in ids)
    x = np.zeros((len(ids), L), dtype=np.int64)
    y = np.zeros((len(ids), L), dtype=np.int64)
    w = np.zeros((len(ids), L), dtype=np.float32)
    for r, i in enumerate(ids):
        seq, wt = examples[i]
        n = len(seq)
        x[r, :n - 1] = seq[:-1]
        y[r, :n - 1] = seq[1:]
        w[r, :n - 1] = wt[1:]      # el peso del objetivo (lo que hay que predecir)
    return x, y, w


def evaluate(model, examples, n=None, token_budget=1000):
    rng = np.random.default_rng(0)
    sel = list(range(len(examples)))[: n or len(examples)]
    sub = [examples[i] for i in sel]
    tot, wsum = 0.0, 0.0
    with no_grad():
        for b in make_batches(sub, token_budget, rng):
            x, y, w = collate(sub, b)
            logits = model(x)
            B, L = x.shape
            loss = cross_entropy(logits.reshape(B * L, -1), y.reshape(-1), w.reshape(-1))
            ws = float(w.sum())
            tot += float(loss.data) * ws
            wsum += ws
            del logits, loss
            gc.collect()   # sin backward() los closures forman ciclos: liberamos a mano
    return tot / max(wsum, 1e-8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=35000)
    ap.add_argument("--lr", type=float, default=2e-3)
    ap.add_argument("--token_budget", type=int, default=768)
    ap.add_argument("--d_model", type=int, default=128)
    ap.add_argument("--layers", type=int, default=6)
    ap.add_argument("--heads", type=int, default=4)
    ap.add_argument("--d_ff", type=int, default=511)
    ap.add_argument("--max_len", type=int, default=384)
    ap.add_argument("--user_weight", type=float, default=0.1)
    ap.add_argument("--eval_every", type=int, default=1000)
    ap.add_argument("--save_every", type=int, default=500)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()

    tok = CharTokenizer.load(os.path.join(ROOT, "data", "vocab.json"))
    train = load_split(os.path.join(ROOT, "data", "dialogues_train.txt"), tok, a.user_weight)
    val = load_split(os.path.join(ROOT, "data", "dialogues_val.txt"), tok, a.user_weight)
    n_tok = sum(len(s) for s, _ in train)
    print(f"train: {len(train)} conversaciones, {n_tok:,} caracteres | val: {len(val)} | vocab {tok.vocab_size}", flush=True)

    np.random.seed(a.seed)
    rng = np.random.default_rng(a.seed)
    model = KermesseModel(tok.vocab_size, a.d_model, a.layers, a.heads, a.d_ff, a.max_len)
    if model.n_params() > MAX_PARAMS:
        raise SystemExit(f"El modelo tendría {model.n_params():,} parámetros; el máximo permitido es {MAX_PARAMS:,}.")
    opt = AdamW(model.named_parameters(), lr=a.lr)
    step0 = 0
    if a.resume and os.path.exists(CKPT + ".npz"):
        model, _, info = load_model(CKPT)
        if model.arch() != KermesseModel(tok.vocab_size, a.d_model, a.layers, a.heads, a.d_ff, a.max_len).arch():
            raise SystemExit("La arquitectura del checkpoint no coincide con los parámetros solicitados.")
        opt = AdamW(model.named_parameters(), lr=a.lr)
        if os.path.exists(CKPT + ".opt.npz"):
            opt.load_state(load_opt_state(CKPT))
        step0 = opt.t
        print(f"reanudando desde el paso {step0}", flush=True)
    print(f"modelo: {model.n_params():,} parámetros | {a.layers} capas x {a.heads} cabezas | d_model={a.d_model} d_ff={a.d_ff}", flush=True)

    t0, step = time.time(), step0
    ema = None
    log = []
    curve_path = os.path.join(ROOT, "checkpoints", "val_curve.json")
    val_history = []
    if a.resume and os.path.isfile(curve_path):
        try:
            val_history = json.load(open(curve_path, encoding="utf-8"))
        except (OSError, ValueError):
            val_history = []
    while step < a.steps:
        for ids in make_batches(train, a.token_budget, rng):
            if step >= a.steps:
                break
            x, y, w = collate(train, ids)
            B, L = x.shape
            logits = model(x)
            loss = cross_entropy(logits.reshape(B * L, -1), y.reshape(-1), w.reshape(-1))
            opt.zero_grad()
            loss.backward()
            gnorm = opt.clip_grad_norm(1.0)
            opt.lr = lr_at(step, a.steps, a.lr)
            opt.step()
            step += 1
            lv = float(loss.data)
            ema = lv if ema is None else 0.95 * ema + 0.05 * lv
            log.append(lv)
            del logits, loss
            if step == 1 or step % 20 == 0:
                el = time.time() - t0
                eta = el / max(1, step - step0) * (a.steps - step)
                print(f"paso {step:5d}/{a.steps} | loss {ema:.3f} | lr {opt.lr:.5f} | |g| {gnorm:.2f} | {el/60:5.1f} min | faltan ~{eta/60:.0f} min", flush=True)
            if step % a.eval_every == 0 or step == a.steps:
                vl = evaluate(model, val, n=150)
                val_history.append({"step": step, "val_loss_150": vl})
                with open(curve_path, "w", encoding="utf-8") as f:
                    json.dump(val_history, f, ensure_ascii=False, indent=1)
                print(f"   >>> validación (150 conv. nunca vistas): loss {vl:.3f}  (perplexity {np.exp(vl):.2f})", flush=True)
            if step % a.save_every == 0 or step == a.steps:
                save_model(model, tok, CKPT, meta={"step": step, "train_loss_ema": ema,
                                                   "release": MODEL_NAME, "parameter_limit": MAX_PARAMS},
                           opt_state=opt.state())
    vl = evaluate(model, val)
    print(f"\nFIN. validación completa: loss {vl:.3f} (perplexity {np.exp(vl):.2f})", flush=True)
    val_history.append({"step": step, "val_loss_full": vl})
    with open(curve_path, "w", encoding="utf-8") as f:
        json.dump(val_history, f, ensure_ascii=False, indent=1)
    save_model(model, tok, CKPT, meta={"step": step, "train_loss_ema": ema, "val_loss": vl,
                                       "release": MODEL_NAME, "parameter_limit": MAX_PARAMS},
               opt_state=opt.state())
    np.save(os.path.join(ROOT, "checkpoints", "losses.npy"), np.array(log))


if __name__ == "__main__":
    main()
