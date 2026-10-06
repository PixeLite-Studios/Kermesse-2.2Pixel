"""
KermesseModel: Transformer decoder (GPT chico) hecho a mano.

  * Entrenamiento: forward(ids) construye el grafo de autograd.
  * Inferencia rápida: step()/prefill() usan una caché de claves/valores (KV-cache)
    en NumPy puro, sin grafo: cada letra nueva cuesta O(contexto) en vez de O(contexto^2).
"""
import numpy as np
import engine
from engine import Tensor
from modules import Module, EmbeddingTable, PositionalEncoding, LayerNorm
from transformer_block import TransformerBlock


def _gelu_np(x):
    return 0.5 * x * (1 + np.tanh(0.7978845608028654 * (x + 0.044715 * x * x * x)))


def _ln_np(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    xc = x - mu
    return xc / np.sqrt((xc * xc).mean(-1, keepdims=True) + eps) * g + b


class KermesseModel(Module):
    def __init__(self, vocab_size, d_model=128, n_layers=4, n_heads=4, d_ff=512, max_len=256):
        self.vocab_size, self.d_model, self.max_len = vocab_size, d_model, max_len
        self.n_heads, self.n_layers, self.d_ff = n_heads, n_layers, d_ff
        self.token_embed = EmbeddingTable(vocab_size, d_model)
        self.pos_enc = PositionalEncoding(d_model, max_len=max_len)
        self.blocks = [TransformerBlock(d_model, n_heads, d_ff, n_layers) for _ in range(n_layers)]
        self.ln_final = LayerNorm(d_model)
        self.output_bias = Tensor(np.zeros(vocab_size), requires_grad=True)

    def arch(self):
        return dict(vocab_size=self.vocab_size, d_model=self.d_model, n_layers=self.n_layers,
                    n_heads=self.n_heads, d_ff=self.d_ff, max_len=self.max_len)

    def n_params(self):
        return int(sum(p.data.size for p in self.parameters()))

    def __call__(self, ids):
        x = self.pos_enc(self.token_embed(ids))
        for blk in self.blocks:
            x = blk(x)
        x = self.ln_final(x)
        return engine.linear_tied(x, self.token_embed.weight, self.output_bias)

    # ------------------ inferencia con KV-cache (NumPy puro) ------------------
    def new_cache(self):
        H, hd = self.n_heads, self.d_model // self.n_heads
        return {"k": [np.zeros((H, self.max_len, hd), np.float32) for _ in range(self.n_layers)],
                "v": [np.zeros((H, self.max_len, hd), np.float32) for _ in range(self.n_layers)],
                "len": 0}

    def step(self, token_id, cache):
        """Procesa UN token y devuelve los logits del siguiente. Actualiza la caché."""
        pos = cache["len"]
        assert pos < self.max_len, "contexto lleno"
        d, H = self.d_model, self.n_heads
        hd = d // H
        x = self.token_embed.weight.data[token_id] * np.sqrt(d) + self.pos_enc.pe[pos]
        for li, blk in enumerate(self.blocks):
            a = blk.attn
            h = _ln_np(x, blk.ln1.gamma.data, blk.ln1.beta.data)
            q = (h @ a.w_q.weight.data + a.w_q.bias.data).reshape(H, hd)
            k = (h @ a.w_k.weight.data + a.w_k.bias.data).reshape(H, hd)
            v = (h @ a.w_v.weight.data + a.w_v.bias.data).reshape(H, hd)
            cache["k"][li][:, pos] = k
            cache["v"][li][:, pos] = v
            K, V = cache["k"][li][:, : pos + 1], cache["v"][li][:, : pos + 1]
            sc = np.einsum("hd,htd->ht", q, K) / np.sqrt(hd)
            sc -= sc.max(-1, keepdims=True)
            p = np.exp(sc)
            p /= p.sum(-1, keepdims=True)
            ctx = np.einsum("ht,htd->hd", p, V).reshape(d)
            x = x + ctx @ a.w_o.weight.data + a.w_o.bias.data
            h = _ln_np(x, blk.ln2.gamma.data, blk.ln2.beta.data)
            h = _gelu_np(h @ blk.ff.fc1.weight.data + blk.ff.fc1.bias.data)
            x = x + h @ blk.ff.fc2.weight.data + blk.ff.fc2.bias.data
        x = _ln_np(x, self.ln_final.gamma.data, self.ln_final.beta.data)
        cache["len"] = pos + 1
        return x @ self.token_embed.weight.data.T + self.output_bias.data

    def prefill(self, ids, cache):
        logits = None
        for t in ids:
            logits = self.step(int(t), cache)
        return logits
