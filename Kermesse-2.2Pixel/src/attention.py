"""Multi-Head Self-Attention causal (usa la atención fusionada del motor)."""
import numpy as np
import engine
from modules import Module, Linear


class MultiHeadAttention(Module):
    def __init__(self, d_model, n_heads, n_layers=1):
        assert d_model % n_heads == 0
        self.d_model, self.n_heads, self.head_dim = d_model, n_heads, d_model // n_heads
        self.w_q = Linear(d_model, d_model)
        self.w_k = Linear(d_model, d_model)
        self.w_v = Linear(d_model, d_model)
        self.w_o = Linear(d_model, d_model, std=0.02 / np.sqrt(2 * n_layers))

    def _split(self, t, B, T):
        return t.reshape(B, T, self.n_heads, self.head_dim).transpose(0, 2, 1, 3)

    def __call__(self, x):
        B, T, _ = x.shape
        q, k, v = (self._split(l(x), B, T) for l in (self.w_q, self.w_k, self.w_v))
        o = engine.causal_attention(q, k, v)
        o = o.transpose(0, 2, 1, 3).reshape(B, T, self.d_model)
        return self.w_o(o)
