"""Bloque Transformer pre-norm: x + Attn(LN(x)), luego x + FFN(LN(x))."""
from modules import Module, LayerNorm, FeedForward
from attention import MultiHeadAttention


class TransformerBlock(Module):
    def __init__(self, d_model, n_heads, d_ff, n_layers=1):
        self.ln1 = LayerNorm(d_model)
        self.attn = MultiHeadAttention(d_model, n_heads, n_layers)
        self.ln2 = LayerNorm(d_model)
        self.ff = FeedForward(d_model, d_ff, n_layers)

    def __call__(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.ff(self.ln2(x))
        return x
