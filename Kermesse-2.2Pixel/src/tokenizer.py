"""
Tokenizador a nivel de carácter + formato de conversación de Kermesse.

IMPORTANTE (uso correcto del dataset): entrenamiento e inferencia pasan por las
MISMAS funciones de este archivo, así el modelo ve en el chat exactamente el mismo
formato con el que aprendió.

Formato interno de una conversación (texto plano):
    \x01 <mensaje del usuario> \n  \x02 <respuesta de Kermesse> \n  \x01 ...
  \x01 = "empieza turno del usuario"      \x02 = "empieza turno de Kermesse"
Todo turno termina en "\n" (así el modelo aprende cuándo parar).
En el archivo legible data/dialogues.txt los turnos se escriben como `vos:` / `kermesse:`.
"""
import json
import re
import unicodedata

USER_TAG, BOT_TAG = "\x01", "\x02"
ROLE_LABELS = {"vos": USER_TAG, "kermesse": BOT_TAG}


class CharTokenizer:
    def __init__(self, chars):
        self.chars = sorted(set(chars))
        self.stoi = {c: i for i, c in enumerate(self.chars)}
        self.itos = {i: c for i, c in enumerate(self.chars)}
        self.vocab_size = len(self.chars)

    def encode(self, text):
        try:
            return [self.stoi[c] for c in text]
        except KeyError as e:
            raise ValueError(f"Carácter fuera del vocabulario: {e}")

    def decode(self, ids):
        return "".join(self.itos[i] for i in ids)

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"chars": self.chars}, f, ensure_ascii=False, indent=1)

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8") as f:
            return cls(json.load(f)["chars"])


# ---------------- normalización de lo que escribe la persona ----------------
def normalize_user_text(text, tok):
    """minúsculas, espacios prolijos, y reemplazo de caracteres que el modelo no conoce."""
    t = text.strip().lower()
    t = re.sub(r"\s+", " ", t)
    out = []
    for ch in t:
        if ch in tok.stoi and ch not in (USER_TAG, BOT_TAG, "\n"):
            out.append(ch)
        else:
            base = unicodedata.normalize("NFD", ch)
            base = "".join(c for c in base if unicodedata.category(c) != "Mn")
            if base and all(c in tok.stoi for c in base):
                out.append(base)
            elif ch.isspace():
                out.append(" ")
            # lo demás (emojis, símbolos raros) se descarta
    return re.sub(r"\s+", " ", "".join(out)).strip()


# ---------------- formato de conversación ----------------
def parse_dialogues(text):
    """Lee dialogues.txt -> lista de conversaciones; cada una = lista de (rol, texto)."""
    convs = []
    for block in text.strip().split("\n\n"):
        turns = []
        for line in block.split("\n"):
            role, _, msg = line.partition(": ")
            if role in ROLE_LABELS and msg:
                turns.append((role, msg))
        if turns:
            convs.append(turns)
    return convs


def conversation_to_text(turns):
    return "".join(ROLE_LABELS[r] + m + "\n" for r, m in turns)


def encode_conversation(tok, turns, user_weight=0.1):
    """-> (ids, pesos). peso 1.0 en lo que dice Kermesse (y su '\\n' final), user_weight en lo del usuario, 0 en etiquetas."""
    ids, w = [], []
    for role, msg in turns:
        tag = ROLE_LABELS[role]
        body = tok.encode(msg + "\n")
        ids.append(tok.stoi[tag]); w.append(0.0)
        ids.extend(body)
        w.extend([1.0 if role == "kermesse" else user_weight] * len(body))
    return ids, w


def build_prompt(history, user_msg):
    """history = [(user, bot), ...] ya normalizado; devuelve el texto listo para el modelo."""
    s = "".join(USER_TAG + u + "\n" + BOT_TAG + b + "\n" for u, b in history)
    return s + USER_TAG + user_msg + "\n" + BOT_TAG
