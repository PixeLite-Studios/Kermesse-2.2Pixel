"""
Motor de autograd de Kermesse. Escrito desde cero sobre NumPy.

Idea central (igual que PyTorch por dentro, pero hecho a mano): cada operación
crea un nodo en un grafo, guardando de qué tensores viene (_prev) y cómo repartir
el gradiente hacia ellos (_backward). backward() recorre el grafo en orden
topológico inverso aplicando la regla de la cadena.

Mejoras respecto a la versión anterior (PixLite):
  * float32 por defecto (2x más rápido en CPU). `set_dtype(np.float64)` para
    los tests de gradiente numérico.
  * Operaciones FUSIONADAS con su backward escrito a mano: linear, layer_norm,
    gelu, causal_attention y cross_entropy ponderada. Antes, LayerNorm eran ~10
    nodos del grafo; ahora es 1. Menos nodos = menos memoria y menos Python.
  * `no_grad()`: contexto para inferencia sin construir grafo.
  * Backward de embedding con one-hot @ grad (mucho más rápido que np.add.at).
"""
import gc
import numpy as np
from contextlib import contextmanager

DTYPE = np.float32
_GRAD_ENABLED = True


def set_dtype(dt):
    global DTYPE
    DTYPE = dt


@contextmanager
def no_grad():
    global _GRAD_ENABLED
    prev = _GRAD_ENABLED
    _GRAD_ENABLED = False
    try:
        yield
    finally:
        _GRAD_ENABLED = prev
        gc.collect()  # en inferencia no hay backward() que corte los ciclos closure<->nodo


def _unbroadcast(grad, shape):
    """Suma el gradiente "grande" de vuelta a la forma del tensor chico (por broadcasting)."""
    while grad.ndim > len(shape):
        grad = grad.sum(axis=0)
    for i, dim in enumerate(shape):
        if dim == 1 and grad.shape[i] != 1:
            grad = grad.sum(axis=i, keepdims=True)
    return grad


class Tensor:
    def __init__(self, data, requires_grad=False, _children=(), _op=""):
        self.data = np.asarray(data, dtype=DTYPE)
        if not _GRAD_ENABLED:
            requires_grad, _children = False, ()
        self.requires_grad = requires_grad
        self.grad = np.zeros_like(self.data) if requires_grad else None
        self._backward = lambda: None
        self._prev = tuple(_children)
        self._op = _op

    @property
    def shape(self):
        return self.data.shape

    def __repr__(self):
        return f"Tensor(shape={self.data.shape}, requires_grad={self.requires_grad}, op='{self._op}')"

    @staticmethod
    def _wrap(x):
        return x if isinstance(x, Tensor) else Tensor(x)

    def _acc(self, g):
        """Acumula gradiente (solo si este tensor lo necesita)."""
        if self.requires_grad:
            if self.grad is None:
                self.grad = np.zeros_like(self.data)
            self.grad += g

    # ---------- operaciones básicas ----------
    def __add__(self, other):
        other = Tensor._wrap(other)
        out = Tensor(self.data + other.data, self.requires_grad or other.requires_grad,
                     (self, other), "+")

        def _backward():
            if self.requires_grad:
                self._acc(_unbroadcast(out.grad, self.data.shape))
            if other.requires_grad:
                other._acc(_unbroadcast(out.grad, other.data.shape))
        out._backward = _backward
        return out

    __radd__ = __add__

    def __neg__(self):
        out = Tensor(-self.data, self.requires_grad, (self,), "neg")

        def _backward():
            self._acc(-out.grad)
        out._backward = _backward
        return out

    def __sub__(self, other):
        return self + (-Tensor._wrap(other))

    def __rsub__(self, other):
        return Tensor._wrap(other) + (-self)

    def __mul__(self, other):
        other = Tensor._wrap(other)
        out = Tensor(self.data * other.data, self.requires_grad or other.requires_grad,
                     (self, other), "*")

        def _backward():
            if self.requires_grad:
                self._acc(_unbroadcast(out.grad * other.data, self.data.shape))
            if other.requires_grad:
                other._acc(_unbroadcast(out.grad * self.data, other.data.shape))
        out._backward = _backward
        return out

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Tensor._wrap(other)
        out = Tensor(self.data / other.data, self.requires_grad or other.requires_grad,
                     (self, other), "/")

        def _backward():
            if self.requires_grad:
                self._acc(_unbroadcast(out.grad / other.data, self.data.shape))
            if other.requires_grad:
                other._acc(_unbroadcast(-out.grad * self.data / (other.data ** 2), other.data.shape))
        out._backward = _backward
        return out

    def __matmul__(self, other):
        other = Tensor._wrap(other)
        out = Tensor(self.data @ other.data, self.requires_grad or other.requires_grad,
                     (self, other), "@")

        def _backward():
            if self.requires_grad:
                self._acc(_unbroadcast(out.grad @ np.swapaxes(other.data, -1, -2), self.data.shape))
            if other.requires_grad:
                other._acc(_unbroadcast(np.swapaxes(self.data, -1, -2) @ out.grad, other.data.shape))
        out._backward = _backward
        return out

    def sum(self, axis=None, keepdims=False):
        out = Tensor(self.data.sum(axis=axis, keepdims=keepdims), self.requires_grad, (self,), "sum")

        def _backward():
            g = out.grad
            if not keepdims and axis is not None:
                g = np.expand_dims(g, axis)
            self._acc(np.ones_like(self.data) * g)
        out._backward = _backward
        return out

    def mean(self, axis=None, keepdims=False):
        count = self.data.size if axis is None else self.data.shape[axis]
        return self.sum(axis=axis, keepdims=keepdims) * (1.0 / count)

    # ---------- forma ----------
    def reshape(self, *shape):
        old_shape = self.data.shape
        out = Tensor(self.data.reshape(*shape), self.requires_grad, (self,), "reshape")

        def _backward():
            self._acc(out.grad.reshape(old_shape))
        out._backward = _backward
        return out

    def transpose(self, *axes):
        out = Tensor(np.transpose(self.data, axes), self.requires_grad, (self,), "transpose")
        inv_axes = tuple(np.argsort(axes))

        def _backward():
            self._acc(np.transpose(out.grad, inv_axes))
        out._backward = _backward
        return out

    # ---------- no linealidades ----------
    def relu(self):
        out = Tensor(np.maximum(self.data, 0.0), self.requires_grad, (self,), "relu")

        def _backward():
            self._acc((self.data > 0).astype(DTYPE) * out.grad)
        out._backward = _backward
        return out

    def gelu(self):
        """GELU (aproximación tanh), fusionada. Más suave que ReLU: entrena mejor modelos chicos."""
        x = self.data
        c = DTYPE(np.sqrt(2.0 / np.pi))
        x2 = x * x
        u = c * (x + DTYPE(0.044715) * x2 * x)
        t = np.tanh(u)
        out = Tensor(DTYPE(0.5) * x * (1 + t), self.requires_grad, (self,), "gelu")

        def _backward():
            du = c * (1 + DTYPE(3 * 0.044715) * x2)
            d = DTYPE(0.5) * (1 + t) + DTYPE(0.5) * x * (1 - t * t) * du
            self._acc(out.grad * d)
        out._backward = _backward
        return out

    def softmax(self, axis=-1):
        shifted = self.data - np.max(self.data, axis=axis, keepdims=True)
        e = np.exp(shifted)
        y = e / np.sum(e, axis=axis, keepdims=True)
        out = Tensor(y, self.requires_grad, (self,), "softmax")

        def _backward():
            g = out.grad
            dot = np.sum(g * y, axis=axis, keepdims=True)
            self._acc(y * (g - dot))
        out._backward = _backward
        return out

    def sqrt(self):
        r = np.sqrt(self.data)
        out = Tensor(r, self.requires_grad, (self,), "sqrt")

        def _backward():
            self._acc(out.grad * 0.5 / r)
        out._backward = _backward
        return out

    def var(self, axis=-1, keepdims=True):
        mu = self.mean(axis=axis, keepdims=True)
        diff = self - mu
        return (diff * diff).mean(axis=axis, keepdims=keepdims)

    def embedding(self, indices):
        """self = tabla de pesos (vocab, d). indices = enteros (no diferenciables)."""
        indices = np.asarray(indices)
        out = Tensor(self.data[indices], self.requires_grad, (self,), "embedding")

        def _backward():
            V = self.data.shape[0]
            flat = indices.reshape(-1)
            onehot = np.zeros((flat.size, V), dtype=DTYPE)
            onehot[np.arange(flat.size), flat] = 1.0
            self._acc(onehot.T @ out.grad.reshape(flat.size, -1))
        out._backward = _backward
        return out

    # ---------- backward ----------
    def backward(self):
        topo, visited = [], set()
        stack = [(self, False)]
        while stack:  # DFS iterativo (sin recursión)
            node, done = stack.pop()
            if done:
                topo.append(node)
                continue
            if id(node) in visited:
                continue
            visited.add(id(node))
            stack.append((node, True))
            for ch in node._prev:
                if id(ch) not in visited:
                    stack.append((ch, False))

        self.grad = np.ones_like(self.data)
        for v in reversed(topo):
            v._backward()
        # cortamos los ciclos closure<->nodo para liberar memoria al instante
        for v in topo:
            v._backward = lambda: None
            v._prev = ()

    def zero_grad(self):
        if self.requires_grad:
            self.grad = np.zeros_like(self.data)


# =====================================================================
#  Operaciones fusionadas (forward + backward escritos a mano)
# =====================================================================
def linear(x, weight, bias=None):
    """y = x @ W + b con UN solo GEMM grande (aplana batch y tiempo)."""
    din, dout = weight.data.shape
    x2 = x.data.reshape(-1, din)
    y = x2 @ weight.data
    if bias is not None:
        y += bias.data
    out = Tensor(y.reshape(*x.data.shape[:-1], dout),
                 x.requires_grad or weight.requires_grad or (bias is not None and bias.requires_grad),
                 (x, weight) + ((bias,) if bias is not None else ()), "linear")

    def _backward():
        g2 = out.grad.reshape(-1, dout)
        if weight.requires_grad:
            weight._acc(x2.T @ g2)
        if bias is not None and bias.requires_grad:
            bias._acc(g2.sum(axis=0))
        if x.requires_grad:
            x._acc((g2 @ weight.data.T).reshape(x.data.shape))
    out._backward = _backward
    return out


def linear_tied(x, emb_weight, bias=None):
    """Cabeza de salida con weight tying: logits = x @ E^T + b, reutilizando la matriz E del embedding."""
    V, d = emb_weight.data.shape
    x2 = x.data.reshape(-1, d)
    y = x2 @ emb_weight.data.T
    if bias is not None:
        y += bias.data
    out = Tensor(y.reshape(*x.data.shape[:-1], V),
                 x.requires_grad or emb_weight.requires_grad,
                 (x, emb_weight) + ((bias,) if bias is not None else ()), "linear_tied")

    def _backward():
        g2 = out.grad.reshape(-1, V)
        if emb_weight.requires_grad:
            emb_weight._acc(g2.T @ x2)
        if bias is not None and bias.requires_grad:
            bias._acc(g2.sum(axis=0))
        if x.requires_grad:
            x._acc((g2 @ emb_weight.data).reshape(x.data.shape))
    out._backward = _backward
    return out


def layer_norm(x, gamma, beta, eps=1e-5):
    """LayerNorm fusionada: un solo nodo, backward analítico."""
    xd = x.data
    mu = xd.mean(axis=-1, keepdims=True)
    xc = xd - mu
    var = (xc * xc).mean(axis=-1, keepdims=True)
    inv = 1.0 / np.sqrt(var + eps)
    xhat = xc * inv
    out = Tensor(xhat * gamma.data + beta.data,
                 x.requires_grad or gamma.requires_grad or beta.requires_grad,
                 (x, gamma, beta), "layer_norm")

    def _backward():
        g = out.grad
        if gamma.requires_grad:
            gamma._acc((g * xhat).reshape(-1, xd.shape[-1]).sum(axis=0))
        if beta.requires_grad:
            beta._acc(g.reshape(-1, xd.shape[-1]).sum(axis=0))
        if x.requires_grad:
            dxhat = g * gamma.data
            m1 = dxhat.mean(axis=-1, keepdims=True)
            m2 = (dxhat * xhat).mean(axis=-1, keepdims=True)
            x._acc(inv * (dxhat - m1 - xhat * m2))
    out._backward = _backward
    return out


def causal_attention(q, k, v):
    """
    Atención causal fusionada. q,k,v: (B, H, T, hd). Devuelve (B, H, T, hd).
    Guarda las probabilidades para el backward (no recalcula).
    """
    B, H, T, hd = q.data.shape
    scale = DTYPE(1.0 / np.sqrt(hd))
    scores = (q.data @ np.swapaxes(k.data, -1, -2)) * scale
    mask = np.triu(np.ones((T, T), dtype=bool), k=1)
    scores = np.where(mask, DTYPE(-1e9), scores)
    scores -= scores.max(axis=-1, keepdims=True)
    p = np.exp(scores)
    p /= p.sum(axis=-1, keepdims=True)
    o = p @ v.data
    out = Tensor(o, q.requires_grad or k.requires_grad or v.requires_grad, (q, k, v), "attn")

    def _backward():
        do = out.grad
        dv = np.swapaxes(p, -1, -2) @ do
        dp = do @ np.swapaxes(v.data, -1, -2)
        ds = p * (dp - (dp * p).sum(axis=-1, keepdims=True)) * scale
        q._acc(ds @ k.data)
        k._acc(np.swapaxes(ds, -1, -2) @ q.data)
        v._acc(dv)
    out._backward = _backward
    return out


def cross_entropy(logits, targets, weights=None):
    """
    Entropía cruzada (softmax + NLL fusionados). `weights` (N,) permite ponderar
    cada posición: 0 = ignorar (padding), 1 = contar plenamente.
    Gradiente: (softmax - one_hot) * w / sum(w).
    """
    targets = np.asarray(targets).reshape(-1)
    N = logits.data.shape[0]
    w = np.ones(N, dtype=DTYPE) if weights is None else np.asarray(weights, dtype=DTYPE).reshape(-1)
    wsum = max(float(w.sum()), 1e-8)
    shifted = logits.data - logits.data.max(axis=-1, keepdims=True)
    e = np.exp(shifted)
    z = e.sum(axis=-1, keepdims=True)
    probs = e / z
    logp = shifted - np.log(z)
    nll = -logp[np.arange(N), targets]
    loss_val = float((nll * w).sum() / wsum)
    out = Tensor(loss_val, logits.requires_grad, (logits,), "cross_entropy")

    def _backward():
        g = probs.copy()
        g[np.arange(N), targets] -= 1.0
        g *= (w / wsum)[:, None]
        logits._acc(g * out.grad)
    out._backward = _backward
    return out


if __name__ == "__main__":
    set_dtype(np.float64)
    a = Tensor(np.random.randn(3, 4), requires_grad=True)
    b = Tensor(np.random.randn(4, 2), requires_grad=True)
    loss = ((a @ b) * 2.0).sum()
    loss.backward()
    print("engine OK, grad a:", a.grad.shape, "grad b:", b.grad.shape)
