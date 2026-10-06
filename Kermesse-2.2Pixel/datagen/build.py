"""
Construye el dataset de Kermesse.   Uso:  python -m datagen.build   (desde la carpeta kermesse/)

Cómo se arma una conversación:
  1. Se elige una "estructura" (1 a 5 unidades). Una unidad es un intercambio simple, un juego de
     varios turnos, un cálculo/dato generado, o un flujo con memoria (nombre, ciudad, gustos...).
  2. Hay transiciones con sentido: después de un saludo suele venir una respuesta de ánimo; después
     de un "estoy bien" suele venir un juego; etc. Así el modelo aprende a mantener el hilo.
  3. Cada mensaje de la persona se "ensucia" (sin tildes, sin signos, abreviaturas, typos...)
     para que Kermesse entienda cómo escribe la gente de verdad. Las respuestas de Kermesse siempre
     salen limpias.
  4. Se valida (formato, caracteres, longitud), se deduplica y se separa un set de validación.
"""
import json
import os
import random
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "src"))

from datagen.lex import add_noise, add_filler
from datagen import c1_identity, c2_chat, c3_games, c4_knowledge, c5_memory
from tokenizer import CharTokenizer, conversation_to_text, USER_TAG, BOT_TAG

MAX_CHARS = 380           # largo máximo de una conversación (incluye etiquetas)
N_TARGET = 17000
VAL_FRAC = 0.03

# ------------------------------------------------------------------ catálogo de unidades
ALL_INTENTS = c1_identity.INTENTS + c2_chat.INTENTS + c3_games.INTENTS + c5_memory.INTENTS
KB_INTENTS = c4_knowledge.INTENTS
BY_NAME = {i["name"]: i for i in ALL_INTENTS + KB_INTENTS}
assert len(BY_NAME) == len(ALL_INTENTS) + len(KB_INTENTS), "nombres de intención duplicados"

MOODS = ["usuario_bien", "usuario_mal", "usuario_regular", "bien_y_vos", "mal_y_vos"]
AFTER = {   # intención -> (prob, [siguientes preferidos])
    "saludo": (0.6, MOODS), "saludo_manana": (0.6, MOODS), "saludo_tarde": (0.6, MOODS), "saludo_noche": (0.6, MOODS), "como_estas": (0.55, MOODS),
    "ya_volvi": (0.5, ["mi_dia", "usuario_bien", "alegria"]),
    "usuario_bien": (0.4, ["__games__"]), "usuario_regular": (0.4, ["__games__", "mi_dia", "tengo_sueno"]), "usuario_mal": (0.5, ["triste", "estres", "enojo", "nervios", "mi_dia", "pedir_animo"]),
    "mal_y_vos": (0.5, ["triste", "estres", "mi_dia", "pedir_animo"]), "bien_y_vos": (0.4, ["__games__", "mi_dia"]),
    "aburrido": (0.9, ["__games__"]), "jugar": (0.9, ["__games__"]), "ok_corto": (0.3, ["__games__", "frases_cortas_charla"]), "si_corto": (0.5, ["__games__"]),
    "no_corto": (0.4, ["frases_cortas_charla", "enseñar_tema"]), "frases_cortas_charla": (0.7, ["respuesta_generica", "mi_dia"]),
    "triste": (0.6, ["pedir_animo", "gracias", "respuesta_generica", "soledad_amigos"]), "pedir_animo": (0.6, ["gracias", "cumplido", "ok_corto"]),
    "nervios": (0.5, ["gracias", "ok_corto", "respuesta_generica"]), "enojo": (0.5, ["respuesta_generica", "gracias"]), "estres": (0.5, ["gracias", "respuesta_generica"]),
    "mi_dia": (0.6, ["respuesta_generica", "gracias", "ok_corto"]), "nombre": (0.0, []), "alegria": (0.7, ["respuesta_generica", "logro"]), "logro": (0.5, ["gracias", "respuesta_generica"]),
    "tengo_hambre": (0.5, ["que_como", "respuesta_generica"]), "cumple": (0.6, ["gracias", "respuesta_generica"]),
    "gracias": (0.3, ["despedida", "ok_corto", "__games__"]), "capacidades": (0.5, ["__games__", "si_corto"]),
}
GAME_FLOWS = [(n, w, f) for (n, w, f) in c3_games.FLOWS]
CATEGORY_W = {"intent": 40, "kb": 10, "games": 16, "gen": 20, "memory": 14}

FILLER_INTENTS = ["gracias", "ok_corto", "sorpresa", "no_entiende_idea", "mi_dia", "respuesta_generica", "respuesta_generica", "cumplido"]


def _user_variant(it, rng):
    return rng.choice(it["users"])


def intent_turns(it, rng):
    return [(_user_variant(it, rng), rng.choice(it["bots"]))]


def filler(rng):
    if rng.random() < 0.7:
        it = BY_NAME["respuesta_generica"]
    else:
        it = BY_NAME[rng.choice(FILLER_INTENTS)]
    return intent_turns(it, rng)


def weighted(rng, items, wi=1):
    tot = sum(x[wi] if isinstance(x, tuple) else x["w"] for x in items)
    r = rng.uniform(0, tot)
    acc = 0
    for x in items:
        acc += x[wi] if isinstance(x, tuple) else x["w"]
        if r <= acc:
            return x
    return items[-1]


def pick_unit(rng, prefer=None, last=None):
    """Devuelve (etiqueta, turnos)."""
    if prefer:
        pool = []
        for p in prefer:
            if p == "__games__":
                pool.append("__games__")
            elif p in BY_NAME:
                pool.append(p)
        c = rng.choice(pool)
        if c == "__games__":
            n, _, f = weighted(rng, GAME_FLOWS)
            return n, f(rng)
        return c, intent_turns(BY_NAME[c], rng)
    cat = rng.choices(list(CATEGORY_W), weights=list(CATEGORY_W.values()))[0]
    if cat == "intent":
        it = weighted(rng, ALL_INTENTS)
        if it["name"] == last:
            it = weighted(rng, ALL_INTENTS)
        return it["name"], intent_turns(it, rng)
    if cat == "kb":
        it = rng.choice(KB_INTENTS)
        return it["name"], intent_turns(it, rng)
    if cat == "games":
        n, _, f = weighted(rng, GAME_FLOWS)
        return n, f(rng)
    if cat == "gen":
        n, _, g = weighted(rng, c4_knowledge.GENERATORS)
        return n, g(rng)
    n, _, f = weighted(rng, c5_memory.MEMORY_FLOWS)
    return n, f(rng, filler)


def make_conv(rng):
    n_units = rng.choices([1, 2, 3, 4, 5], weights=[26, 30, 22, 14, 8])[0]
    turns, labels = [], []
    prefer = None
    # abre con saludo la mitad de las veces
    if rng.random() < 0.45:
        it = weighted(rng, [i for i in ALL_INTENTS if i["tag"] == "open"])
        labels.append(it["name"]); turns += intent_turns(it, rng)
        prefer_cfg = AFTER.get(it["name"])
        prefer = prefer_cfg[1] if prefer_cfg and rng.random() < prefer_cfg[0] else None
        n_units -= 1
    last = labels[-1] if labels else None
    for _ in range(max(n_units, 0) if labels else n_units):
        lab, t = pick_unit(rng, prefer, last)
        labels.append(lab); turns += t
        cfg = AFTER.get(lab)
        prefer = cfg[1] if cfg and cfg[1] and rng.random() < cfg[0] else None
        last = lab
    if rng.random() < 0.22:
        it = weighted(rng, [i for i in ALL_INTENTS if i["tag"] == "close"])
        labels.append(it["name"]); turns += intent_turns(it, rng)
    return labels, turns


def dirty_user(text, rng):
    t = text.lower() if rng.random() < 0.15 else add_noise(text, rng)
    t = add_filler(t, rng)
    return t.lower()


def finalize(turns, rng):
    out = []
    for u, b in turns:
        out.append(("vos", dirty_user(u, rng)))
        out.append(("kermesse", b))
    return out


def fits(conv):
    return len(conversation_to_text(conv)) <= MAX_CHARS


def trim_to_fit(conv):
    while len(conv) > 2 and not fits(conv):
        conv = conv[:-2]
    return conv if fits(conv) else None


def validate(conv, allowed=None):
    for role, msg in conv:
        assert role in ("vos", "kermesse")
        assert "\n" not in msg and msg.strip() == msg and msg, repr(msg)
        assert "  " not in msg, repr(msg)
        if role == "kermesse":
            assert len(msg) >= 2


def main(seed=7):
    rng = random.Random(seed)
    seen, convs, label_count = set(), [], Counter()
    attempts = 0
    while len(convs) < N_TARGET and attempts < N_TARGET * 8:
        attempts += 1
        labels, turns = make_conv(rng)
        conv = trim_to_fit(finalize(turns, rng))
        if conv is None:
            continue
        validate(conv)
        key = conversation_to_text(conv)
        if key in seen:
            continue
        seen.add(key)
        convs.append(conv)
        for l in labels:
            label_count[l] += 1
    rng.shuffle(convs)
    n_val = int(len(convs) * VAL_FRAC)
    val, train = convs[:n_val], convs[n_val:]

    def dump(path, cs):
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n\n".join("\n".join(f"{r}: {m}" for r, m in c) for c in cs) + "\n")

    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    dump(os.path.join(ROOT, "data", "dialogues_train.txt"), train)
    dump(os.path.join(ROOT, "data", "dialogues_val.txt"), val)

    full = "".join(conversation_to_text(c) for c in convs)
    chars = sorted(set(full))
    tok = CharTokenizer(chars)
    tok.save(os.path.join(ROOT, "data", "vocab.json"))
    bot_chars = sum(len(m) for c in convs for r, m in c if r == "kermesse")
    stats = dict(
        conversaciones=len(convs), train=len(train), val=len(val), caracteres_totales=len(full), caracteres_respuestas_kermesse=bot_chars,
        turnos_kermesse=sum(len(c) // 2 for c in convs), vocab=tok.vocab_size,
        largo_medio_conv=round(len(full) / len(convs), 1),
        respuestas_kermesse_unicas=len({m for c in convs for r, m in c if r == "kermesse"}),
        mensajes_usuario_unicos=len({m for c in convs for r, m in c if r == "vos"}),
        intenciones=len(ALL_INTENTS) + len(KB_INTENTS), top_unidades=label_count.most_common(25))
    with open(os.path.join(ROOT, "data", "dataset_stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in stats.items() if k != "top_unidades"}, ensure_ascii=False, indent=1))
    return convs


if __name__ == "__main__":
    main()
