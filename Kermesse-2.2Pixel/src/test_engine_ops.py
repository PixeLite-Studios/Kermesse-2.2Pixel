"""
Verificación numérica del motor: compara el gradiente analítico (backward escrito
a mano) contra diferencias finitas, para TODAS las operaciones (incluidas las fusionadas),
y comprueba que la inferencia con KV-cache da exactamente lo mismo que el forward completo.
"""
import numpy as np
import engine
from engine import Tensor, cross_entropy

engine.set_dtype(np.float64)   # float64 para que el chequeo numérico sea limpio
np.random.seed(0)
ALL_OK = True


def num_grad(f, x, eps=1e-6):
    g = np.zeros_like(x)
    for idx in np.ndindex(*x.shape):
        o = x[idx]
        x[idx] = o + eps; fp = f()
        x[idx] = o - eps; fm = f()
        x[idx] = o
        g[idx] = (fp - fm) / (2 * eps)
    return g


def check(name, build, shapes, tol=1e-6):
    """build(*tensors) -> Tensor escalar. Verifica el grad de cada entrada."""
    global ALL_OK
    arrs = [np.random.randn(*s) for s in shapes]
    ts = [Tensor(a.copy(), requires_grad=True) for a in arrs]
    build(*ts).backward()
    worst = 0.0
    for i, a in enumerate(arrs):
        def f():
            return float(build(*[Tensor(b) for b in arrs]).data)
        worst = max(worst, np.abs(ts[i].grad - num_grad(f, a)).max())
    ok = worst < tol
    ALL_OK &= ok
    print(f"[{'OK' if ok else 'FALLO'}] {name:28s} dif. máx = {worst:.2e}")


W = {}
def wsum(t, key):  # reduce a escalar con pesos aleatorios fijos (así el chequeo es sensible a todo)
    if key not in W:
        W[key] = np.random.randn(*t.shape)
    return (t * Tensor(W[key])).sum()

check("add/mul/sub/div", lambda a, b: wsum((a * b - a) / (b * b + 2.0), "ops"), [(3, 4), (3, 4)])
check("matmul", lambda a, b: wsum(a @ b, "mm"), [(2, 3, 4), (4, 5)])
check("reshape+transpose", lambda a: wsum(a.reshape(2, 2, 3).transpose(1, 0, 2), "rt"), [(2, 6)])
check("gelu", lambda a: wsum(a.gelu(), "gelu"), [(4, 5)])
check("relu", lambda a: wsum(a.relu(), "relu"), [(4, 5)])
check("softmax", lambda a: wsum(a.softmax(-1), "sm"), [(3, 6)])
check("embedding", lambda w: wsum(w.embedding(np.array([[1, 2, 1], [0, 3, 3]])), "emb"), [(5, 4)])
check("linear (fusionada)", lambda x, w, b: wsum(engine.linear(x, w, b), "lin"), [(2, 3, 4), (4, 5), (5,)])
check("linear_tied", lambda x, e, b: wsum(engine.linear_tied(x, e, b), "lt"), [(2, 3, 4), (6, 4), (6,)])
check("layer_norm (fusionada)", lambda x, g, b: wsum(engine.layer_norm(x, g, b), "ln"), [(2, 3, 6), (6,), (6,)])
check("causal_attention", lambda q, k, v: wsum(engine.causal_attention(q, k, v), "att"),
      [(2, 2, 5, 3), (2, 2, 5, 3), (2, 2, 5, 3)])
tg = np.array([1, 0, 3, 2, 2, 1])
wt = np.array([1, 0.1, 0, 1, 1, 0.5])
check("cross_entropy ponderada", lambda x: cross_entropy(x, tg, wt), [(6, 4)])

# ---------- modelo completo ----------
from kermesse_model import KermesseModel
np.random.seed(1)
m = KermesseModel(vocab_size=11, d_model=8, n_layers=2, n_heads=2, d_ff=16, max_len=16)
for p in m.parameters():                 # sacamos los parámetros de la escala diminuta del init
    p.data = np.random.randn(*p.data.shape) * 0.3
ids = np.random.randint(0, 11, size=(2, 7))
tgt = np.random.randint(0, 11, size=14)
loss = cross_entropy(m(ids).reshape(14, 11), tgt)
loss.backward()
worst = 0.0
for name, p in m.named_parameters():
    if p.data.size > 80:                 # chequeo exhaustivo sólo en los chicos; el resto por muestreo
        idxs = [tuple(np.random.randint(0, s) for s in p.data.shape) for _ in range(6)]
    else:
        idxs = list(np.ndindex(*p.data.shape))
    for idx in idxs:
        o = p.data[idx]
        p.data[idx] = o + 1e-6; fp = float(cross_entropy(m(ids).reshape(14, 11), tgt).data)
        p.data[idx] = o - 1e-6; fm = float(cross_entropy(m(ids).reshape(14, 11), tgt).data)
        p.data[idx] = o
        worst = max(worst, abs(p.grad[idx] - (fp - fm) / 2e-6))
ok = worst < 1e-6
ALL_OK &= ok
print(f"[{'OK' if ok else 'FALLO'}] {'modelo completo (todos los params)':28s} dif. máx = {worst:.2e}")

# ---------- KV-cache == forward completo ----------
with engine.no_grad():
    full = m(ids[:1]).data[0]
cache = m.new_cache()
step_logits = np.stack([m.step(int(t), cache) for t in ids[0]])
d = np.abs(full - step_logits).max()
ok = d < 1e-4
ALL_OK &= ok
print(f"[{'OK' if ok else 'FALLO'}] {'KV-cache == forward completo':28s} dif. máx = {d:.2e}")

print("\nTODO OK ✔" if ALL_OK else "\nHAY FALLOS ✘")
raise SystemExit(0 if ALL_OK else 1)
