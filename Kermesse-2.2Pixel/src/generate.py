"""
Motor de conversación de Kermesse (inferencia). Usa la caché K/V: cada letra nueva es barata.

    from generate import Kermesse
    k = Kermesse()                 # carga checkpoints/kermesse_21pixel (los pesos no cambian en 2.2)
    print(k.reply("hola"))
    for ch in k.reply_stream("contame un chiste"): print(ch, end="", flush=True)
"""
import os
import numpy as np

from checkpoint import load_model
from tokenizer import normalize_user_text, build_prompt, USER_TAG, BOT_TAG
from assistant_logic import LocalAssistant, MODEL_NAME, VERSION, CREATOR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CKPT = os.path.join(ROOT, "checkpoints", "kermesse_21pixel")
DEFAULT_MEMORY_FILE = os.path.join(ROOT, "data", "user_memory.json")
MAX_MODEL_PARAMS = 2_000_000


class Kermesse:
    def __init__(self, ckpt=DEFAULT_CKPT, temperature=0.6, top_k=20, top_p=0.92,
                 seed=None, reserve=170, memory_path=DEFAULT_MEMORY_FILE):
        self.model, self.tok, self.info = load_model(ckpt)
        if self.model.n_params() > MAX_MODEL_PARAMS:
            raise ValueError(
                f"El checkpoint tiene {self.model.n_params():,} parámetros; "
                f"el límite de Kermesse es {MAX_MODEL_PARAMS:,}."
            )
        if not np.isfinite(temperature) or not 0.05 <= temperature <= 2.0:
            raise ValueError("La temperatura debe ser un número entre 0.05 y 2.0.")
        self.temperature, self.top_k, self.top_p = temperature, top_k, top_p
        self.rng = np.random.default_rng(seed)
        self.reserve = reserve            # lugar que se deja libre para la respuesta
        self.history = []                 # [(mensaje_usuario_normalizado, respuesta)]
        self.logic = LocalAssistant(memory_path=memory_path)
        self._ban = [self.tok.stoi[USER_TAG], self.tok.stoi[BOT_TAG]]
        self._nl = self.tok.stoi["\n"]

    def reset(self, clear_persistent=True):
        self.history = []
        self.logic.reset(clear_saved=clear_persistent)

    # ---------------------------------------------------------- muestreo
    def _sample(self, logits, allow_newline):
        z = logits.astype(np.float64) / max(self.temperature, 1e-3)
        z[self._ban] = -np.inf
        if not allow_newline:
            z[self._nl] = -np.inf
        if self.top_k and self.top_k < len(z):
            kth = np.partition(z, -self.top_k)[-self.top_k]
            z[z < kth] = -np.inf
        p = np.exp(z - z.max())
        p /= p.sum()
        if self.top_p < 1.0:
            order = np.argsort(-p)
            cum = np.cumsum(p[order])
            cut = order[np.searchsorted(cum, self.top_p) + 1:]
            p[cut] = 0.0
            p /= p.sum()
        return int(self.rng.choice(len(p), p=p))

    def _build_ids(self, user_norm):
        hist = list(self.history)
        while True:
            prompt = build_prompt(hist, user_norm)
            if len(prompt) <= self.model.max_len - self.reserve or not hist:
                break
            hist.pop(0)                    # olvida lo más viejo (memoria corta, como dice ella)
        return self.tok.encode(prompt)

    # ---------------------------------------------------------- API
    def reply_stream(self, text):
        user = normalize_user_text(text, self.tok)
        if not user:
            msg = "¿Me decís algo? Acá estoy para charlar."
            for ch in msg:
                yield ch
            return
        user = user[:160]
        answer = self.logic.respond(text, user, self.model.n_params(), self.rng)
        if answer is not None:
            self.history.append((user, answer))
            for ch in answer:
                yield ch
            return
        ids = self._build_ids(user)
        cache = self.model.new_cache()
        logits = self.model.prefill(ids, cache)
        out = []
        while cache["len"] < self.model.max_len:
            nxt = self._sample(logits, allow_newline=len(out) >= 2)
            if nxt == self._nl:
                break
            ch = self.tok.itos[nxt]
            out.append(ch)
            yield ch
            logits = self.model.step(nxt, cache)
        self.history.append((user, "".join(out).strip()))

    def reply(self, text):
        return "".join(self.reply_stream(text)).strip()
