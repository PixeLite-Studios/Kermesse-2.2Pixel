"""
Capas de red neuronal sobre nuestro propio motor (engine.py).
Cada módulo guarda sus Tensors-parámetro y sabe transformar entrada -> salida.
"""
import numpy as np
import engine
from engine import Tensor


class Module:
    def named_parameters(self, prefix=""):
        """Devuelve [(nombre, Tensor)] en orden determinista (se usa para guardar/cargar)."""
        out = []
        for name, attr in vars(self).items():
            full = f"{prefix}{name}"
            if isinstance(attr, Tensor) and attr.requires_grad:
                out.append((full, attr))
            elif isinstance(attr, Module):
                out.extend(attr.named_parameters(full + "."))
            elif isinstance(attr, list):
                for i, item in enumerate(attr):
                    if isinstance(item, Module):
                        out.extend(item.named_parameters(f"{full}.{i}."))
        return out

    def parameters(self):
        return [p for _, p in self.named_parameters()]

    def zero_grad(self):
        for p in self.parameters():
            p.zero_grad()


class Linear(Module):
    def __init__(self, din, dout, bias=True, std=0.02):
        self.weight = Tensor(np.random.normal(0, std, size=(din, dout)), requires_grad=True)
        self.bias = Tensor(np.zeros(dout), requires_grad=True) if bias else None

    def __call__(self, x):
        return engine.linear(x, self.weight, self.bias)


class EmbeddingTable(Module):
    def __init__(self, vocab_size, d_model, std=0.05):
        self.weight = Tensor(np.random.normal(0, std, size=(vocab_size, d_model)), requires_grad=True)
        self.d_model = d_model

    def __call__(self, indices):
        return self.weight.embedding(indices) * float(np.sqrt(self.d_model))


class LayerNorm(Module):
    def __init__(self, d_model, eps=1e-5):
        self.gamma = Tensor(np.ones(d_model), requires_grad=True)
        self.beta = Tensor(np.zeros(d_model), requires_grad=True)
        self.eps = eps

    def __call__(self, x):
        return engine.layer_norm(x, self.gamma, self.beta, self.eps)


class FeedForward(Module):
    """Dos capas lineales con GELU en el medio."""

    def __init__(self, d_model, d_ff, n_layers=1):
        self.fc1 = Linear(d_model, d_ff)
        # proyección de salida escalada (estilo GPT-2) para estabilizar el camino residual
        self.fc2 = Linear(d_ff, d_model, std=0.02 / np.sqrt(2 * n_layers))

    def __call__(self, x):
        return self.fc2(self.fc1(x).gelu())


class PositionalEncoding:
    """Seno/coseno fijo (sin parámetros entrenables)."""

    def __init__(self, d_model, max_len=256):
        pe = np.zeros((max_len, d_model))
        pos = np.arange(0, max_len)[:, None]
        div = np.exp(np.arange(0, d_model, 2) * (-np.log(10000.0) / d_model))
        pe[:, 0::2] = np.sin(pos * div)
        pe[:, 1::2] = np.cos(pos * div)
        self.pe = pe.astype(np.float32)

    def __call__(self, x):
        return x + Tensor(self.pe[: x.shape[1]].astype(engine.DTYPE))
