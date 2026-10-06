"""Guardar/cargar modelos en formato .npz + .json (portable: sin pickle, sirve en PC y en Termux)."""
import json
import os
import numpy as np
from kermesse_model import KermesseModel
from tokenizer import CharTokenizer


def save_model(model, tok, path_prefix, meta=None, opt_state=None):
    arrays = {n: p.data.astype(np.float32) for n, p in model.named_parameters()}
    tmp = path_prefix + ".tmp.npz"
    np.savez(tmp, **arrays)
    os.replace(tmp, path_prefix + ".npz")
    info = {"arch": model.arch(), "vocab_chars": tok.chars, "n_params": model.n_params(), "meta": meta or {}}
    with open(path_prefix + ".json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=1)
    if opt_state is not None:
        o = {"t": np.array(opt_state["t"])}
        for i, (m, v) in enumerate(zip(opt_state["m"], opt_state["v"])):
            o[f"m{i}"], o[f"v{i}"] = m, v
        np.savez(path_prefix + ".opt.tmp.npz", **o)
        os.replace(path_prefix + ".opt.tmp.npz", path_prefix + ".opt.npz")


def load_model(path_prefix):
    with open(path_prefix + ".json", encoding="utf-8") as f:
        info = json.load(f)
    model = KermesseModel(**info["arch"])
    data = np.load(path_prefix + ".npz")
    for n, p in model.named_parameters():
        p.data = data[n].astype(np.float32)
    return model, CharTokenizer(info["vocab_chars"]), info


def load_opt_state(path_prefix):
    o = np.load(path_prefix + ".opt.npz")
    n = (len(o.files) - 1) // 2
    return {"t": int(o["t"]), "m": [o[f"m{i}"] for i in range(n)], "v": [o[f"v{i}"] for i in range(n)]}
