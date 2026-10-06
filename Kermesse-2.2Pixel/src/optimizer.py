"""AdamW hecho a mano + recorte de gradiente + scheduler coseno con warmup."""
import numpy as np


class AdamW:
    def __init__(self, named_params, lr=3e-3, betas=(0.9, 0.98), eps=1e-8, weight_decay=0.02):
        self.names = [n for n, _ in named_params]
        self.params = [p for _, p in named_params]
        self.lr, (self.b1, self.b2), self.eps, self.wd = lr, betas, eps, weight_decay
        self.m = [np.zeros_like(p.data) for p in self.params]
        self.v = [np.zeros_like(p.data) for p in self.params]
        # weight decay solo en matrices de pesos (no en biases, LayerNorm ni embedding)
        self.decay = [p.data.ndim == 2 and "token_embed" not in n for n, p in named_params]
        self.t = 0

    def clip_grad_norm(self, max_norm):
        total = np.sqrt(sum(float((p.grad.astype(np.float64) ** 2).sum()) for p in self.params))
        if total > max_norm:
            s = max_norm / (total + 1e-6)
            for p in self.params:
                p.grad *= s
        return total

    def step(self):
        self.t += 1
        c1, c2 = 1 - self.b1 ** self.t, 1 - self.b2 ** self.t
        for i, p in enumerate(self.params):
            g = p.grad
            self.m[i] *= self.b1; self.m[i] += (1 - self.b1) * g
            self.v[i] *= self.b2; self.v[i] += (1 - self.b2) * g * g
            upd = (self.m[i] / c1) / (np.sqrt(self.v[i] / c2) + self.eps)
            if self.decay[i]:
                upd += self.wd * p.data
            p.data -= (self.lr * upd).astype(p.data.dtype)

    def zero_grad(self):
        for p in self.params:
            p.zero_grad()

    def state(self):
        return {"t": self.t, "m": self.m, "v": self.v}

    def load_state(self, st):
        self.t = st["t"]
        self.m = [x.copy() for x in st["m"]]
        self.v = [x.copy() for x in st["v"]]


def lr_at(step, total, peak, warmup=60, floor=0.08):
    if step < warmup:
        return peak * (step + 1) / warmup
    prog = (step - warmup) / max(1, total - warmup)
    return peak * (floor + (1 - floor) * 0.5 * (1 + np.cos(np.pi * min(1.0, prog))))
