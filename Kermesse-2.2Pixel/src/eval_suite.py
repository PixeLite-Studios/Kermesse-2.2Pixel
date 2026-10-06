"""
Evaluación AUTOMÁTICA de Kermesse con respuestas verificables (no es "a ojo").
    python eval_suite.py            -> imprime el reporte y lo guarda en checkpoints/eval_report.json

Cada prueba hace preguntas con una respuesta correcta conocida y cuenta aciertos.
Las pruebas de 'generalización' usan datos que NO están en el entrenamiento (nombres inventados,
países sin capital en el dataset, preguntas de las que no debería saber nada).
"""
import json
import os
import random
import re
import sys


from generate import Kermesse, ROOT

sys.path.insert(0, ROOT)
from datagen.c4_knowledge import CAPITALS

K = Kermesse(temperature=0.5, seed=1, memory_path=None)
rng = random.Random(99)
REPORT = {}
EXAMPLES = {}


def ask(*msgs):
    K.reset()
    out = []
    for m in msgs:
        out.append(K.reply(m))
    return out


def run(name, cases, check, show=3):
    ok, fails = 0, []
    for c in cases:
        res = check(c)
        if res[0]:
            ok += 1
        else:
            fails.append(res[1])
    REPORT[name] = {"aciertos": ok, "total": len(cases), "porcentaje": round(100 * ok / len(cases), 1)}
    EXAMPLES[name] = fails[:show]
    print(f"{name:42s} {ok:3d}/{len(cases):3d}  ({REPORT[name]['porcentaje']:5.1f}%)", flush=True)


# 1) Capitales (conocimiento memorizado)
def chk_cap(c):
    pais, cap = c
    r = ask(f"¿cuál es la capital de {pais}?")[0]
    return cap.lower() in r.lower(), (pais, cap, r)
run("Capitales (49 países)", CAPITALS, chk_cap)

# 2) Cuentas con operandos NUEVOS (se sortean al azar; muchos combos no estaban en el entrenamiento)
probs = []
for _ in range(40):
    op = rng.choice("+-x")
    a, b = rng.randint(0, 50), rng.randint(0, 50)
    if op == "-" and b > a: a, b = b, a
    if op == "x": a, b = rng.randint(0, 10), rng.randint(0, 10)
    probs.append((a, op, b, {"+": a + b, "-": a - b, "x": a * b}[op]))
def chk_math(c):
    a, op, b, r = c
    out = ask(f"¿cuánto es {a} {op} {b}?")[0]
    return re.search(rf"\b{r}\b", out) is not None, (f"{a}{op}{b}", r, out)
run("Cuentas (suma, resta, multiplicación)", probs, chk_math)

# 2b) Expresiones más largas, porcentajes, potencias, raíces y números escritos.
EXT_MATH = [
    ("¿cuánto es (18 + 12) / 5?", 6),
    ("¿cuánto es treinta y dos más siete?", 39),
    ("¿cuánto es 15% de 80?", 12),
    ("raíz cuadrada de 81", 9),
    ("cinco al cubo", 125),
    ("¿cuánto es 2,5 por 4?", 10),
    ("¿cuánto es 7 módulo 4?", 3),
    ("¿cuánto es 2 elevado a 10?", 1024),
]
def chk_extended_math(c):
    q, expected = c
    out = ask(q)[0]
    ok = re.search(rf"\bEl resultado es {re.escape(str(expected))}\b", out, re.I) is not None
    return ok, (q, expected, out)
run("Cálculo extendido (8 expresiones)", EXT_MATH, chk_extended_math)

# 3) Memoria del nombre con nombres que NO existen en el dataset
NEW_NAMES = ["Aurelio", "Ludmila", "Kaito", "Bernardita", "Anselmo", "Dorotea", "Evaristo", "Maximina", "Lisandra", "Teodoro", "Casandra", "Ildefonso"]
def chk_name(n):
    r = ask(f"me llamo {n.lower()}", "¿cómo me llamo?")
    return (n in r[0] and n in r[1]), (n, r)
run("Recordar un nombre nuevo (generaliza)", NEW_NAMES, chk_name)

# 4) Piedra, papel o tijera: ¿decide bien quién gana?
beats = {"piedra": "tijera", "papel": "piedra", "tijera": "papel"}
def chk_rps(u):
    r = ask("jugamos piedra papel o tijera", u)[1]
    m = re.search(r"(?:saqué|Elegí|sacamos|elegimos) (piedra|papel|tijera)", r)
    if not m:
        return False, (u, r)
    b = m.group(1)
    if u == b: good = "mpat" in r
    elif beats[u] == b: good = bool(re.search(r"[Gg]anaste", r))
    else: good = bool(re.search(r"[Gg]an[eé] yo|gané", r))
    return good, (u, r)
run("Piedra-papel-tijera: resultado correcto", ["piedra", "papel", "tijera"] * 8, chk_rps)

# 5) Adivinanza: reconoce la respuesta correcta
RID = [("Blanca por dentro, verde por fuera", "pera"), ("Tengo agujas y no sé coser", "reloj"), ("Si me nombras, desaparezco", "silencio")]
def chk_riddle(c):
    r = ask("una adivinanza")[0]
    return "?" in r, (r,)
run("Adivinanza: propone una y la formula", list(range(8)), chk_riddle)

# 6) Identidad estable
def chk_id(c):
    q, pat = c
    r = ask(q)[0]
    return re.search(pat, r, re.I) is not None, (q, r)
run("Identidad (nombre, tipo, parámetros)", [("¿cómo te llamás?", "kermesse"), ("¿quién sos?", "kermesse|ia|inteligencia"), ("¿sos una persona?", "no soy|ia|programa"),
                                             ("¿cuántos parámetros tenés?", "mil|parámetros"), ("¿quién te creó?", "pixelite"), ("¿tenés internet?", "no")] * 2, chk_id)

# 7) Honestidad: no inventa lo que no sabe
UNK = ["¿quién ganó el mundial de 1986?", "¿cuántos habitantes tiene brasil?", "¿qué hora es?", "¿cómo está el clima hoy?", "¿cuánto está el dólar?", "¿quién es el presidente de francia?",
       "¿cómo se cocina un risotto?", "¿qué es la mecánica cuántica?", "¿cuál es la capital de mongolia?", "¿qué pasó ayer en las noticias?", "¿cuál es el mejor lenguaje de programación?", "¿cuántos años tiene el sol?"]
def chk_unk(q):
    r = ask(q)[0]
    ok = re.search(r"no sé|no tengo|no puedo|se me escapa|prefiero|no me|perdón|no conozco|sin respuesta|no lo sé|mejor|no estoy|no se", r, re.I) is not None
    return ok, (q, r)
run("Honestidad: admite lo que no sabe", UNK, chk_unk)

# 8) Empatía: tono correcto ante tristeza / alegría
def chk_emp(c):
    q, pat = c
    r = ask(q)[0]
    return re.search(pat, r, re.I) is not None, (q, r)
run("Empatía (tristeza, alegría, nervios)", [("estoy muy triste", "lamento|siento|escuch|abrazo"), ("me siento solo", "acá|escuch|compañ|amig"), ("tengo una buena noticia", "alegr|contame|genial|qué bueno"),
                                              ("estoy nervioso por un examen", "respir|tranqui|nervios"), ("aprobé el examen", "felicit|orgullo|genial|festej"), ("estoy re cansado", "descans|cansancio|dorm|uf")] * 2, chk_emp)

# 9) Robustez a cómo escribe la gente (sin tildes, sin signos, abreviaturas)
ROB = [("ola q tal", "hola|buenas|qué|cómo|alegr"), ("kien eres", "kermesse|ia"), ("cual es la capital de peru", "lima"), ("cuanto es 6 por 7", "42"), ("contame un chiste porfa", "\\?|jaja|¿"), ("grax", "nada|gusto|hay de qué|a vos"),
       ("q haces", "charl|hacés|vos"), ("adios", "chau|adiós|hasta|nos vemos")]
run("Robustez: tipeo informal / sin tildes", ROB, chk_emp)

# 10) Memoria de contexto en varios turnos (ciudad / edad / color)
def chk_mem(c):
    t1, t2, pat = c
    r = ask(t1, t2)
    return re.search(pat, r[1], re.I) is not None, (t1, t2, r)
run("Memoria de contexto (ciudad, edad, color)", [("vivo en córdoba", "¿dónde vivo?", "córdoba"), ("tengo 34 años", "¿cuántos años tengo?", "34"), ("mi color favorito es el verde", "¿cuál es mi color favorito?", "verde"),
                                                   ("vivo en lima", "¿de dónde soy?", "lima"), ("tengo 21 años", "¿qué edad tengo?", "21"), ("me gusta dibujar", "¿qué me gusta hacer?", "dibujar")], chk_mem)

# 10b) Relaciona una persona con su parentesco y un dato explícito.
def chk_relation(_):
    r = ask("mi hermana se llama Camila y tiene 30 años", "¿quién es Camila?", "¿qué edad tiene ella?")
    ok = "Camila" in r[1] and "hermana" in r[1] and "Camila" in r[2] and "30" in r[2]
    return ok, tuple(r)
run("Relaciones y referencia entre turnos", [0], chk_relation)

# 11) Chiste: devuelve un chiste y reacciona al "jaja"
def chk_joke(c):
    r = ask("contame un chiste", "jajaja")
    return ("?" in r[0] or "—" in r[0] or "." in r[0]) and re.search(r"otro|chiste|jaja|alegr|risa", r[1], re.I) is not None, (r,)
run("Chiste + reacción al 'jaja'", list(range(8)), chk_joke)

tot_ok = sum(v["aciertos"] for v in REPORT.values()); tot = sum(v["total"] for v in REPORT.values())
print(f"\nTOTAL: {tot_ok}/{tot} = {100*tot_ok/tot:.1f}%")
REPORT["_total"] = {"aciertos": tot_ok, "total": tot, "porcentaje": round(100 * tot_ok / tot, 1)}
REPORT["_fallos_de_ejemplo"] = {k: [list(map(str, f)) for f in v] for k, v in EXAMPLES.items()}
json.dump(REPORT, open(os.path.join(ROOT, "checkpoints", "eval_report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
