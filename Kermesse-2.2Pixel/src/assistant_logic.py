"""Funciones locales verificables para complementar el modelo conversacional."""
import ast
import copy
import json
import math
import os
import re
import sys
import unicodedata


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

VERSION = "2.2"
MODEL_NAME = "Kermesse-2.2Pixel"
CREATOR = "PixeLite"

try:
    from datagen.c4_knowledge import CAPITALS, UNKNOWN_CAPITALS
except Exception:
    CAPITALS, UNKNOWN_CAPITALS = [], []


def fold(text):
    """Normaliza para comparar sin depender de tildes, mayúsculas o puntuación."""
    text = unicodedata.normalize("NFD", text.casefold())
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def _display(value):
    words = value.strip().split()
    return " ".join(w if w.lower() in ("de", "del", "la", "las", "los") and i else w.capitalize()
                    for i, w in enumerate(words))


def _clean_capture(value):
    value = re.split(r"[,?.!;]", value, maxsplit=1)[0]
    value = re.sub(r"\s+(?:y|pero)\s+(?:vos|tu|el|ella|yo)\b.*$", "", value, flags=re.I)
    return value.strip(" \t\n:")


def _eval_math_node(node, depth=0):
    """Evalúa un árbol aritmético acotado; nunca ejecuta código del usuario."""
    if depth > 20:
        raise ValueError("expresión demasiado profunda")
    if isinstance(node, ast.Expression):
        return _eval_math_node(node.body, depth + 1)
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        value = node.value
        if abs(value) > 1e12:
            raise ValueError("número demasiado grande")
        return value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _eval_math_node(node.operand, depth + 1)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp):
        left = _eval_math_node(node.left, depth + 1)
        right = _eval_math_node(node.right, depth + 1)
        if isinstance(node.op, ast.Add):
            result = left + right
        elif isinstance(node.op, ast.Sub):
            result = left - right
        elif isinstance(node.op, ast.Mult):
            result = left * right
        elif isinstance(node.op, ast.Div):
            result = left / right
        elif isinstance(node.op, ast.FloorDiv):
            result = left // right
        elif isinstance(node.op, ast.Mod):
            result = left % right
        elif isinstance(node.op, ast.Pow):
            if abs(right) > 12:
                raise ValueError("exponente demasiado grande")
            result = left ** right
        else:
            raise ValueError("operación no permitida")
        if isinstance(result, complex) or not math.isfinite(result) or abs(result) > 1e18:
            raise ValueError("resultado fuera de rango")
        return result
    raise ValueError("expresión no permitida")


def _format_number(value):
    if isinstance(value, int) or (isinstance(value, float) and value.is_integer()):
        return str(int(value))
    return f"{value:.8g}"


def _pick(rng, choices):
    return choices[int(rng.integers(0, len(choices)))]


_NUMBER_WORDS = {
    "cero": 0, "un": 1, "uno": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4,
    "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
    "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15,
    "dieciseis": 16, "diecisiete": 17, "dieciocho": 18, "diecinueve": 19,
    "veinte": 20, "veintiuno": 21, "veintidos": 22, "veintitres": 23,
    "veinticuatro": 24, "veinticinco": 25, "veintiseis": 26, "veintisiete": 27,
    "veintiocho": 28, "veintinueve": 29, "treinta": 30, "cuarenta": 40,
    "cincuenta": 50, "sesenta": 60, "setenta": 70, "ochenta": 80,
    "noventa": 90, "cien": 100, "ciento": 100, "doscientos": 200,
    "trescientos": 300, "quinientos": 500, "mil": 1000,
}
for _tens, _base in (("treinta", 30), ("cuarenta", 40), ("cincuenta", 50),
                     ("sesenta", 60), ("setenta", 70), ("ochenta", 80), ("noventa", 90)):
    for _unit in range(1, 10):
        _unit_name = ("uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve")[_unit - 1]
        _NUMBER_WORDS[f"{_tens} y {_unit_name}"] = _base + _unit


class LocalAssistant:
    """Reglas pequeñas y sin red para tareas donde una respuesta exacta importa."""

    def __init__(self, memory_path=None):
        self.memory_path = memory_path
        self.memory_save_error = False
        self.facts = {}
        self.rps_active = False
        self.pending_joke = False
        self.pending_riddle = None
        self.last_capital_country = None
        self._load_memory()
        self.capitals = {fold(country): city for country, city in CAPITALS}
        self.capital_names = {fold(country): country for country, _ in CAPITALS}
        self.unknown_capitals = {fold(country) for country in UNKNOWN_CAPITALS}
        self.capitals.update({
            "eeuu": "Washington D. C.",
            "usa": "Washington D. C.",
            "estados unidos de america": "Washington D. C.",
            "corea del sur": "Seúl",
            "bolivia": "Sucre / La Paz",
        })
        self.capital_names.update({
            "eeuu": "Estados Unidos",
            "usa": "Estados Unidos",
            "estados unidos de america": "Estados Unidos",
        })
        self.reverse_capitals = {fold(city): country for country, city in CAPITALS}

    def reset(self, clear_saved=False):
        self.facts = {}
        self.rps_active = False
        self.pending_joke = False
        self.pending_riddle = None
        self.last_capital_country = None
        self.memory_save_error = False
        if clear_saved and self.memory_path and os.path.exists(self.memory_path):
            try:
                os.remove(self.memory_path)
            except OSError:
                self.memory_save_error = True

    def _load_memory(self):
        if not self.memory_path or not os.path.isfile(self.memory_path):
            return
        try:
            with open(self.memory_path, encoding="utf-8") as f:
                stored = json.load(f)
            allowed = {"nombre", "ciudad", "edad", "color", "hobby", "ocupacion", "relaciones"}
            self.facts = {k: v for k, v in stored.items()
                          if k in allowed and isinstance(v, (str, dict))}
        except (OSError, ValueError, TypeError):
            self.facts = {}

    def _save_memory(self):
        if not self.memory_path:
            return
        temp_path = self.memory_path + ".tmp"
        try:
            directory = os.path.dirname(self.memory_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(self.facts, f, ensure_ascii=False, indent=2)
            os.replace(temp_path, self.memory_path)
            self.memory_save_error = False
        except OSError:
            self.memory_save_error = True
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except OSError:
                pass

    def _memory_notice(self):
        if self.memory_save_error:
            return "No pude guardarlo en disco, así que lo recordaré mientras esta charla siga abierta."
        if self.memory_path:
            return "Lo guardé solo en este dispositivo."
        return "Lo tendré presente mientras charlamos."

    def context_summary(self):
        parts = []
        for key, label in (("nombre", "te llamás"), ("ciudad", "vivís en"),
                           ("edad", "tenés"), ("color", "tu color favorito es"),
                           ("hobby", "te gusta"), ("ocupacion", "trabajás como")):
            value = self.facts.get(key)
            if value:
                suffix = " años" if key == "edad" else ""
                parts.append(f"{label} {value}{suffix}")
        for person in self.facts.get("relaciones", {}).values():
            if isinstance(person, dict) and person.get("nombre") and person.get("relacion"):
                detail = f"{person['nombre']} es tu {person['relacion']}"
                if person.get("edad"):
                    detail += f" y tiene {person['edad']} años"
                parts.append(detail)
        if not parts:
            return ""
        return "Recuerdo que " + "; ".join(parts) + "."

    def _remember(self, text, raw):
        # No convertir preguntas sobre un dato en nuevas declaraciones (p. ej.,
        # "¿qué me gusta hacer?" no debe sustituir el hobby por "hacer").
        if "?" in raw:
            return
        # Las relaciones explícitas se guardan por separado de los datos de la
        # persona usuaria, para poder resolver luego "¿quién es Camila?".
        role_names = {
            "madre": "mamá", "mama": "mamá", "padre": "papá", "papa": "papá",
            "hermano": "hermano", "hermana": "hermana", "hijo": "hijo",
            "hija": "hija", "pareja": "pareja", "esposo": "esposo",
            "esposa": "esposa", "amigo": "amigo", "amiga": "amiga",
            "perro": "perro", "gata": "gata", "gato": "gato", "mascota": "mascota",
        }
        role_pattern = r"(madre|mamá|mama|padre|papá|papa|hermano|hermana|hijo|hija|pareja|esposo|esposa|amigo|amiga|perro|gata|gato|mascota)"
        relation_match = re.search(
            rf"\bmi\s+{role_pattern}\s+se llama\s+([^,?.!;]+)", raw, flags=re.I
        )
        if not relation_match:
            # La forma "mi hermana es Camila" es ambigua si todo está en
            # minúsculas; solo se acepta como nombre si está escrito como tal.
            relation_match = re.search(
                rf"\bmi\s+{role_pattern}\s+es\s+([A-ZÁÉÍÓÚÑ][^,?.!;]*)", raw
            )
        if relation_match:
            role = role_names[fold(relation_match.group(1))]
            raw_name = re.sub(r"\s+(?:y|pero)\s+.*$", "", relation_match.group(2), flags=re.I)
            raw_name = re.split(r"\s+(?:tiene|cumplio|vive|trabaja|estudia)\b", raw_name, maxsplit=1, flags=re.I)[0]
            person_name = _display(_clean_capture(raw_name))
            if person_name:
                relations = dict(self.facts.get("relaciones", {}))
                person = dict(relations.get(fold(person_name), {}))
                person.update({"nombre": person_name, "relacion": role})
                age = re.search(r"\btiene\s+(\d{1,3})\s*(?:anos?|anitos)\b", text)
                if age:
                    person["edad"] = age.group(1)
                relations[fold(person_name)] = person
                self.facts["relaciones"] = relations

        # Vincular datos nuevos con entidades que ya fueron presentadas.
        relations = dict(self.facts.get("relaciones", {}))
        for key, person in list(relations.items()):
            age = re.search(rf"\b{re.escape(fold(person.get('nombre', '')))}\s+(?:tiene|cumplio)\s+(\d{{1,3}})\s*(?:anos?|anitos)\b", text)
            if age:
                updated = dict(person)
                updated["edad"] = age.group(1)
                relations[key] = updated
                self.facts["relaciones"] = relations
        # Capturar nombres solo ante una declaración explícita evita confundir
        # "soy feliz", "soy de Lima" o "soy una persona" con un nombre.
        patterns = (
            r"\bme llamo\s+([^,?.!;]+)",
            r"\bmi nombre es\s+([^,?.!;]+)",
            r"\bme dicen\s+([^,?.!;]+)",
        )
        value = None
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.I)
            if match:
                value = _clean_capture(match.group(1))
                break
        if value:
            value = re.sub(r"\s+(?:mucho gusto|un gusto|encantad[oa])\b.*$", "", value, flags=re.I)
            value = " ".join(value.split()[:3])
            if 1 <= len(value) <= 42:
                self.facts["nombre"] = _display(value)

        match = re.search(
            r"\b(?:vivo en|mi ciudad es|soy de|naci en|estoy en)\s+([^,?.!;]+)",
            text, flags=re.I
        )
        if match:
            raw_match = re.search(
                r"\b(?:vivo en|mi ciudad es|soy de|nací en|estoy en)\s+([^,?.!;]+)",
                raw, flags=re.I
            )
            city = _clean_capture(raw_match.group(1) if raw_match else match.group(1))
            if city and len(city) <= 60:
                self.facts["ciudad"] = _display(city)

        match = re.search(r"\b(?:tengo|cumpli)\s+(\d{1,3})\s*(?:anos?|anitos)\b", text)
        if match:
            self.facts["edad"] = match.group(1)

        match = re.search(r"\b(?:mi color favorito es|mi color preferido es)\s+(?:el\s+|la\s+)?([a-z ]+)", text)
        if match:
            color = _clean_capture(match.group(1))
            if color:
                self.facts["color"] = color

        match = re.search(r"\b(?:mi hobby es|mi pasatiempo es|en mi tiempo libre me gusta)\s+([^,?.!;]+)", text)
        if match:
            hobby = _clean_capture(match.group(1))
            if hobby:
                self.facts["hobby"] = hobby
        elif re.search(r"\bme gusta\b", text) and not re.search(r"\b(?:color|comer)\b", text):
            match = re.search(r"\bme gusta\s+([^,?.!;]+)", text)
            if match:
                hobby = _clean_capture(match.group(1))
                if hobby and len(hobby) <= 55:
                    self.facts["hobby"] = hobby

        match = re.search(r"\b(?:trabajo como|trabajo de|me dedico a)\s+([^,?.!;]+)", text)
        if match:
            occupation = _clean_capture(match.group(1))
            if occupation and len(occupation) <= 60:
                self.facts["ocupacion"] = occupation

        # Los nombres se conservan en el registro con la escritura que se tecleó,
        # si la entrada original tenía mayúsculas.
        if "nombre" in self.facts:
            for pattern in patterns:
                match = re.search(pattern, raw, flags=re.I)
                if match:
                    original = _clean_capture(match.group(1))
                    original = re.sub(r"\s+(?:mucho gusto|un gusto|encantad[oa])\b.*$", "", original, flags=re.I)
                    original = " ".join(original.split()[:3])
                    if original and any(ch.isupper() for ch in original):
                        self.facts["nombre"] = _display(original)
                    break

    def _math(self, text):
        root = re.search(r"\b(?:raiz cuadrada de|raiz de|sqrt)\s*(-?\d+(?:\.\d+)?)", text)
        if root:
            number = float(root.group(1))
            if number < 0:
                return "La raíz cuadrada real de un número negativo no está definida."
            return f"El resultado es {_format_number(math.sqrt(number))}. ¿Querés que resolvamos otra?"

        percentage = re.search(
            r"(-?\d+(?:[.,]\d+)?)\s*(?:%|por ciento)\s*(?:de|del)\s*(-?\d+(?:[.,]\d+)?)", text
        )
        if percentage:
            a = float(percentage.group(1).replace(",", "."))
            b = float(percentage.group(2).replace(",", "."))
            return f"El resultado es {_format_number(a * b / 100)}. ¿Querés que te muestre el paso a paso?"

        source = text
        source = source.replace("¿", "")
        source = re.sub(r"\b(?:raiz cuadrada de|raiz de|sqrt)\s*", "", source)
        source = re.sub(r"\b(?:el )?doble de\s+(-?\d+(?:[.,]\d+)?)", r"2 * \1", source)
        source = re.sub(r"\b(?:el )?triple de\s+(-?\d+(?:[.,]\d+)?)", r"3 * \1", source)
        source = re.sub(r"\s+al cuadrado\b", " ** 2", source)
        source = re.sub(r"\s+al cubo\b", " ** 3", source)
        source = re.sub(r"\s+elevado a\s+", " ** ", source)
        source = re.sub(r"\s+a la potencia de\s+", " ** ", source)
        for word, value in sorted(_NUMBER_WORDS.items(), key=lambda pair: len(pair[0]), reverse=True):
            source = re.sub(rf"\b{re.escape(word)}\b", str(value), source)
        source = re.sub(r"(?<=\d),(?=\d)", ".", source)
        source = re.sub(r"^(?:cuanto es|cuanto da|cuanto resulta|calcula|resuelve)\s+", "", source)
        source = re.sub(r"\bdividido(?: por)?\b|\bentre\b", "/", source)
        source = re.sub(r"\bmodulo\b|\bmod\b", "%", source)
        source = re.sub(r"\b(?:mas)\b", "+", source)
        source = re.sub(r"\bmenos\b", "-", source)
        source = re.sub(r"\b(?:por|veces)\b", "*", source)
        source = source.replace("×", "*").replace("^", "**")
        source = re.sub(r"(?<=\d)\s*x\s*(?=[\d(])", "*", source)
        source = source.replace("¿", "").replace("?", "").strip()

        # Evaluar solo aritmética; una frase con números como "tengo 34 años"
        # no coincide con la gramática y nunca se interpreta como expresión.
        if not re.fullmatch(r"[0-9\s.+*/()%\-]+", source):
            return None
        try:
            value = _eval_math_node(ast.parse(source, mode="eval"))
        except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
            if re.search(r"/\s*0+(?:\.0*)?$", source):
                return "No se puede dividir por cero."
            if re.search(r"\d.*(?:[+\-*/%^]|\*\*).*\d", source):
                return "No pude resolver esa expresión con seguridad. Escribime la cuenta de otra forma y la revisamos."
            return None
        return f"El resultado es {_format_number(value)}. ¿Querés ver el paso a paso o probar otra cuenta?"

    def _capital(self, text):
        text = text.strip("¿¡ ").rstrip("?.! ")
        match = re.search(r"\bcapital\s+(?:de|del)\s+(.+)$", text)
        if not match:
            match = re.search(r"^(?:y\s+)?(?:la\s+de|la\s+capital\s+de)\s+(.+)$", text)
        if not match and self.last_capital_country and re.fullmatch(r"(?:y\s+)?(?:la capital|la de ella)", text.strip()):
            country = self.last_capital_country
            city = self.capitals.get(country)
            if city:
                name = self.capital_names.get(country, _display(country))
                return f"La capital de {name} es {city}."
            return f"No tengo un dato verificado sobre la capital de {_display(country)}; prefiero no inventarlo."
        if match:
            country = _clean_capture(match.group(1))
            country = re.sub(r"\s+(?:kermesse|porfa|por favor)$", "", country).strip()
            city = self.capitals.get(country)
            if city:
                self.last_capital_country = fold(country)
                if fold(country) == "bolivia":
                    return "Bolivia tiene dos capitales: Sucre es la capital constitucional y La Paz, sede del gobierno."
                official_name = self.capital_names.get(country, _display(country))
                return f"La capital de {official_name} es {city}."
            if fold(country) in self.unknown_capitals:
                self.last_capital_country = fold(country)
                return f"No tengo un dato verificado sobre la capital de {_display(country)}; prefiero no inventarlo."
            self.last_capital_country = fold(country)
            return "No tengo un dato verificado para esa capital; prefiero no inventarlo."

        match = re.search(r"\b(?:de que pais es capital|capital de que pais es)\s+(.+)$", text)
        if match:
            city = _clean_capture(match.group(1))
            country = self.reverse_capitals.get(city)
            if country:
                return f"{_display(city)} es la capital de {country}."
        return None

    def _memory(self, text):
        relations = self.facts.get("relaciones", {})
        age_question = re.search(r"\b(?:cuantos anos tiene|que edad tiene)\s+(.+)$", text)
        if age_question:
            wanted = _clean_capture(age_question.group(1))
            person = relations.get(fold(wanted))
            if person is None and wanted in ("el", "ella", "mi hermana", "mi hermano", "mi mama", "mi papa", "mi pareja"):
                person = next((p for p in reversed(list(relations.values()))
                               if wanted in ("el", "ella") or fold(p.get("relacion", "")) in wanted), None)
            if person:
                if person.get("edad"):
                    return f"Me contaste que {person['nombre']} tiene {person['edad']} años."
                return f"Todavía no me contaste la edad de {person['nombre']}."

        name_question = re.search(r"\bcomo se llama mi\s+(hermano|hermana|mama|madre|papa|padre|pareja|hijo|hija|mascota|perro|gato)\b", text)
        if name_question:
            role = {"mama": "mamá", "madre": "mamá", "papa": "papá", "padre": "papá"}.get(
                name_question.group(1), name_question.group(1))
            person = next((p for p in reversed(list(relations.values()))
                           if fold(p.get("relacion", "")) == fold(role)), None)
            if person:
                return f"Me contaste que {person['nombre']} es tu {person['relacion']}."

        who_match = re.search(r"\bquien es\s+(.+)$", text)
        if who_match:
            wanted = _clean_capture(who_match.group(1))
            person = relations.get(fold(wanted))
            if person:
                return f"Me contaste que {person['nombre']} es tu {person['relacion']}."
            for person in relations.values():
                role = fold(person.get("relacion", ""))
                if fold(wanted) in (role, "mi " + role, "tu " + role):
                    return f"Me contaste que {person['nombre']} es tu {person['relacion']}."

        asks = (
            (("como me llamo", "mi nombre", "de mi nombre", "te acordas de mi nombre"),
             "nombre", "Todavía no me dijiste tu nombre."),
            (("donde vivo", "de donde soy", "mi ciudad", "en que ciudad estoy", "donde estoy"),
             "ciudad", "Todavía no me contaste dónde vivís."),
            (("cuantos anos tengo", "que edad tengo", "mi edad"),
             "edad", "Todavía no me contaste tu edad."),
            (("mi color favorito", "que color me gusta", "mi color preferido"),
             "color", "Todavía no me contaste tu color favorito."),
            (("que me gusta hacer", "cual es mi hobby", "mi pasatiempo"),
             "hobby", "Todavía no me contaste qué te gusta hacer."),
            (("en que trabajo", "a que me dedico", "cual es mi trabajo"),
             "ocupacion", "Todavía no me contaste en qué trabajás."),
        )
        for patterns, key, missing in asks:
            if any(p in text for p in patterns):
                if key not in self.facts:
                    return missing
                value = self.facts[key]
                if key == "nombre":
                    return f"Te llamás {value}; me lo contaste antes."
                if key == "ciudad":
                    return f"Me dijiste que vivís en {value}."
                if key == "edad":
                    return f"Me contaste que tenés {value} años."
                if key == "color":
                    return f"Tu color favorito es el {value}."
                if key == "ocupacion":
                    return f"Me contaste que trabajás como {value}."
                return f"Me contaste que te gusta {value}."

        if any(p in text for p in ("que sabes de mi", "que recordas de mi", "que te conte de mi")):
            summary = self.context_summary()
            return summary if summary else "Todavía no me contaste datos personales para recordar."
        return None

    def _identity(self, text):
        """Creador y nombre: respuestas fijas para que no dependan del modelo neuronal."""
        if re.search(r"\bpixelite\b", text) and re.search(r"\b(?:quien|que)\s+(?:es|era)\b", text):
            return f"{CREATOR} es quien me creó: diseñó mi motor, me entrenó y me armó desde cero."
        if re.search(
            r"\bquien\s+(?:te\s+|(?=(?:\w+\s+){1,2}(?:a\s+)?(?:kermesse|esta\s+ia)\b))(?:creo|hizo|armo|programo|disenio|diseno|desarrollo|invento|entreno|construyo|fabrico|escribio)\b"
            r"|\bquien\s+(?:es|fue)\s+(?:tu|el)\s+(?:creador|autor|desarrollador|programador|dueno)\b"
            r"|\bquien\s+esta\s+detras\b|\b(?:tenes|tienes)\s+(?:un\s+)?creador\b"
            r"|\bde\s+donde\s+(?:saliste|surgiste)\b|\bquien\s+te\s+dio\s+vida\b",
            text,
        ):
            return f"Me creó {CREATOR}. Armó todo desde cero: el tokenizador, el motor y el entrenamiento."
        return None

    def respond(self, raw, normalized, n_params, rng):
        text = fold(normalized)
        if not text:
            return None

        if self.rps_active:
            choice = next((x for x in ("piedra", "papel", "tijera") if re.search(rf"\b{x}\b", text)), None)
            if choice:
                self.rps_active = False
                bot = ("piedra", "papel", "tijera")[int(rng.integers(0, 3))]
                if choice == bot:
                    return f"Elegí {bot}. ¡Empatamos! ¿Revancha?"
                if (choice, bot) in (("piedra", "tijera"), ("papel", "piedra"), ("tijera", "papel")):
                    return f"Elegí {bot}. ¡Ganaste vos! ¿Revancha?"
                return f"Elegí {bot}. ¡Gané yo esta vez! ¿Revancha?"

        if all(word in text for word in ("piedra", "papel", "tijera")):
            self.rps_active = True
            return "¡Dale! Elegí: piedra, papel o tijera."

        # Parsear la entrada original: la normalización del tokenizador descarta
        # símbolos que no están en el vocabulario, como %, aunque sean clave para la cuenta.
        arithmetic = self._math(fold(raw))
        if arithmetic:
            return arithmetic

        identity = self._identity(text)
        if identity:
            return identity

        capital = self._capital(text)
        if capital:
            if capital.startswith("No tengo"):
                return capital
            return capital + " ¿Querés que busquemos otra?"

        previous_facts = copy.deepcopy(self.facts)
        self._remember(text, raw)
        if self.facts != previous_facts:
            self._save_memory()
            if self.facts.get("nombre") != previous_facts.get("nombre"):
                return _pick(rng, (
                    f"¡Mucho gusto, {self.facts['nombre']}! {self._memory_notice()}",
                    f"¡Hola, {self.facts['nombre']}! {self._memory_notice()} ¿Qué tema te gustaría conversar?",
                ))
            if self.facts.get("ciudad") != previous_facts.get("ciudad"):
                return _pick(rng, (
                    f"¡Qué bueno! Me dijiste que vivís en {self.facts['ciudad']}. ¿Qué es lo mejor de estar ahí?",
                    f"Anotado: vivís en {self.facts['ciudad']}. ¿Hay algún lugar de ahí que te guste especialmente?",
                ))
            if self.facts.get("edad") != previous_facts.get("edad"):
                return f"Gracias por contarme; me quedo con que tenés {self.facts['edad']} años. ¿Querés que recuerde algo más?"
            if self.facts.get("color") != previous_facts.get("color"):
                return f"¡Lindo color! Anoto que tu favorito es el {self.facts['color']}. ¿Qué te gusta de ese color?"
            if self.facts.get("hobby") != previous_facts.get("hobby"):
                return f"¡Qué bueno! Me contaste que te gusta {self.facts['hobby']}. ¿Qué parte disfrutás más?"
            if self.facts.get("ocupacion") != previous_facts.get("ocupacion"):
                return f"Interesante, trabajás como {self.facts['ocupacion']}. {self._memory_notice()} ¿Qué parte de ese trabajo te gusta más?"
            if self.facts.get("relaciones") != previous_facts.get("relaciones"):
                person = list(self.facts["relaciones"].values())[-1]
                return f"Gracias por contármelo: {person['nombre']} es tu {person['relacion']}. {self._memory_notice()}"
        remembered = self._memory(text)
        if remembered:
            return remembered

        if any(p in text for p in ("cuantos parametros", "cuantos millones de parametros", "cuantos parametros tenes")):
            return f"Tengo {n_params:,} parámetros entrenados; estoy por debajo del límite de 2 millones.".replace(",", ".")
        if any(p in text for p in ("como te llamas", "como te dicen", "quien sos", "quien eres", "kien eres", "kien sos")):
            return f"Soy {MODEL_NAME}, una IA conversacional pequeña creada por {CREATOR} que funciona localmente."
        if any(p in text for p in ("sos una persona", "eres una persona", "sos humano", "eres humano")):
            return "No soy una persona; soy un programa de inteligencia artificial que conversa."
        if any(p in text for p in ("tenes internet", "tienes internet", "tenes acceso a internet", "estas conectada a internet")):
            return "No tengo acceso a internet en esta versión; todo funciona sin conexión."
        if any(p in text for p in ("que sabes hacer", "que podes hacer", "que puedes hacer")):
            return "Puedo conversar, hacer cuentas, responder capitales que tengo guardadas, recordar algunos datos localmente y jugar."

        if self.pending_joke and re.search(r"\b(ja(?:ja)+|je(?:je)+|me rei|que gracioso)\b", text):
            self.pending_joke = False
            return "¡Me alegra haberte hecho reír! ¿Querés que te cuente otro?"
        if any(p in text for p in ("contame un chiste", "cuentame un chiste", "decime un chiste", "un chiste")):
            self.pending_joke = True
            jokes = (
                "¿Qué le dice una iguana a su hermana gemela? ¡Iguanita!",
                "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
                "¿Por qué el libro de matemáticas estaba triste? Porque tenía muchos problemas.",
                "¿Qué le dijo una taza a otra? ¿Qué taza-ciendo?",
            )
            return jokes[int(rng.integers(0, len(jokes)))]

        if "adivinanza" in text or "acertijo" in text:
            self.pending_riddle = "pera"
            return "Blanca por dentro, verde por fuera. Si querés que te lo diga, esperá. ¿Qué es?"
        if self.pending_riddle and any(x in text for x in ("pera", "reloj", "silencio")):
            answer = self.pending_riddle
            self.pending_riddle = None
            if answer in text:
                return "¡Sí, era la pera! ¿Querés otra adivinanza?"
            return "Casi: la respuesta era la pera. ¿Querés otra adivinanza?"

        if re.search(r"\b(?:bien|todo bien|tranqui)\b", text) and re.search(r"\b(?:y vos|y tu)\b", text):
            return "Gracias por preguntar; estoy lista para charlar. ¡Qué bueno que estés bien! ¿Qué te gustaría hacer hoy?"
        if re.search(r"\b(?:mas o menos|regular)\b", text):
            return "Entiendo. ¿Querés contarme qué haría que el día mejore un poco, o preferís distraerte?"
        if re.search(r"\bestoy aburrid[oa]\b|\bme aburro\b", text):
            return "Podemos jugar a piedra-papel-tijera, probar una adivinanza o buscar un tema que te interese. ¿Cuál te tienta?"
        if any(p in text for p in ("dame animo", "necesito animo", "decime algo lindo")):
            return "No tenés que resolver todo de una vez. Elegí un paso pequeño y empezá por ahí; si querés, lo pensamos juntos."
        if re.search(r"\b(?:mal|muy mal)\b", text):
            return "Uy, lo siento. Si te sirve, contame qué pasó; también podemos cambiar de tema un rato."

        if re.search(r"\b(triste|tristeza|deprimid[oa])\b", text):
            return "Lamento que estés pasando por esto. Acá estoy para escucharte. ¿Querés contarme qué pasó?"
        if re.search(r"\bme siento sol[oa]\b", text):
            return "Siento que te estés sintiendo así. Estoy acá para escucharte; ¿querés contarme qué pasó?"
        if "buena noticia" in text or "estoy feliz" in text or "estoy contento" in text:
            return "¡Qué alegría! Me encanta que tengas una buena noticia. ¿Qué pasó?"
        if "nervios" in text or "nervioso" in text or "nerviosa" in text:
            return "Es normal sentir nervios. Probá respirar hondo: inhalá cuatro segundos y soltá el aire en seis. ¿Qué te preocupa?"
        if "aprobe" in text or "aprobe el examen" in text:
            return "¡Felicitaciones por aprobar! Se nota todo el esfuerzo que pusiste. ¡A festejar!"
        if "cansado" in text or "cansada" in text or "agotado" in text:
            return "Uf, estar tan cansado pesa. Si podés, tomate un rato para descansar; te lo merecés."

        if re.search(r"\b(ola|hola|buenas|buenos dias|buenas tardes|buenas noches)\b", text):
            return _pick(rng, (
                "¡Hola! Me alegra charlar con vos. ¿Qué te gustaría contarme hoy?",
                "¡Buenas! ¿Cómo viene tu día: tranquilo, movido o una mezcla?",
                "¡Hola! Estoy acá. ¿Venís con una pregunta o con ganas de conversar?",
            ))
        if text.strip() in ("grax", "gracias", "muchas gracias", "te agradezco"):
            return "¡De nada! Me alegra poder ayudarte."
        if re.search(r"\b(adios|chau|hasta luego|nos vemos)\b", text):
            return "¡Hasta pronto! Volvé cuando quieras."
        if text.strip() in ("q haces", "que haces", "que haces?"):
            return "Estoy acá para charlar con vos, responder preguntas y jugar. ¿Qué te gustaría hacer?"

        if re.search(r"\b(?:como se cocina|como cocinar|como preparar|receta de)\b", text):
            return "No tengo una receta verificada en los datos locales de esta versión; prefiero no inventar los pasos."
        if any(p in text for p in (
            "que hora es", "que dia es hoy", "como esta el clima", "que clima hace",
            "cuanto esta el dolar", "noticias de hoy", "que paso ayer en las noticias",
            "quien es el presidente", "cuantos habitantes tiene", "cuantos anos tiene el sol",
            "quien gano el mundial", "quien gano mundial", "mejor lenguaje de programacion",
        )):
            return "No tengo internet ni datos actualizados, así que no puedo confirmar eso. Prefiero no inventar."
        return None
