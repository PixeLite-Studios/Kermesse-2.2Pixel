"""Léxico compartido, ruido de usuario y helpers para armar el dataset de Kermesse."""
import random
import re


def I(name, users, bots, w=1, tag=""):
    """Una intención: muchas formas de decir lo mismo (users) y muchas de responder (bots)."""
    return dict(name=name, users=users, bots=bots, w=w, tag=tag)


NAMES = """lucía mateo valentina santiago camila sofía martín julieta nicolás agustina joaquín florencia tomás micaela facundo
rocío lautaro carolina diego paula andrés daniela javier mariana gonzalo natalia sebastián victoria emiliano belén bruno
antonella franco milagros ignacio romina matías luciana federico noelia maximiliano melina ezequiel pilar rodrigo abril
leandro malena esteban tamara pablo ximena hernán brenda alan jimena cristian ailén ramiro celeste gabriel silvana david
fernanda marcos regina adrián ana luis carla jorge elena carlos marta miguel laura pedro sara raúl inés óscar rosa iván
clara hugo nora simón olivia thiago emma benjamín mía lola juan maría josé lucas alma nico fede cande mili pau male jime
nacho pipo tito lu gise sol bianca renata mora catalina julián emilia dante ulises juana lara noah ivana kevin yamila
cecilia sergio patricio andrea claudia gustavo mauro ariel analía vanesa darío lorena marcelo alejandra rubén elisa
guadalupe candela morena ámbar rafael ernesto eugenia josefina trinidad zoe leo gael bautista lisandro tobías samanta""".split()

CITIES = """buenos aires|córdoba|rosario|mendoza|lima|montevideo|santiago|bogotá|quito|madrid|barcelona|guadalajara|asunción|caracas|panamá
la plata|tucumán|salta|cusco|arequipa|medellín|cali|valparaíso|sevilla|valencia|bilbao|monterrey|puebla|la paz|cochabamba
mar del plata|neuquén|santa fe|paraná|trujillo|piura|guayaquil|cuenca|punta del este|concepción|temuco|maracaibo|cartagena
barranquilla|san juan|bariloche|ushuaia|posadas|corrientes|resistencia|tegucigalpa|managua|la habana|santo domingo""".replace("\n", "|").split("|")

FOODS = """pizza|milanesa|empanadas|asado|pasta|tacos|ceviche|hamburguesa|sushi|arepas|paella|ñoquis|locro|chocolate|helado|tortilla
fideos|pollo|lasaña|sándwich|ensalada|papas fritas|choripán|medialunas|alfajores|flan|tarta|guiso|pastel|churros|arroz con pollo
canelones|ravioles|pancho|dulce de leche|torta|brownie|polenta""".replace("\n", "|").split("|")

HOBBIES = """leer|dibujar|cocinar|correr|bailar|jugar videojuegos|tocar la guitarra|ver series|escribir|nadar|andar en bici|pintar
sacar fotos|caminar|ir al gimnasio|jugar al fútbol|tejer|cantar|ver películas|escuchar música|viajar|jugar al básquet|hacer yoga
jardinería|armar rompecabezas|jugar al ajedrez|programar|patinar|salir a pasear|hacer teatro|mirar fútbol""".replace("\n", "|").split("|")

PETS = "firulais|luna|simba|toby|mora|max|nala|rocky|manchita|pelusa|coco|lola|bruno|kira|oreo|tigre|chispa|mia|canela|rufo|pepe|milo|nube|thor|frida".split("|")
ANIMALS = ["perro", "gato", "conejo", "tortuga", "pájaro", "hámster", "pez", "loro"]
COLORS = ["rojo", "azul", "verde", "amarillo", "violeta", "naranja", "rosa", "negro", "celeste", "blanco", "turquesa", "marrón"]


def cap(s):
    return s[:1].upper() + s[1:]


def cap_words(s):
    return " ".join(cap(w) for w in s.split(" "))


# ---------------- ruido en lo que escribe el usuario (robustez) ----------------
_ACC = str.maketrans("áéíóúü", "aeiouu")
_ABBR = {"que": "q", "qué": "q", "porque": "xq", "para": "pa", "también": "tmb", "tambien": "tmb",
         "hola": "ola", "bien": "bn", "gracias": "grax", "mucho": "muxo", "cómo": "como", "dónde": "donde",
         "con": "c", "pero": "pro", "cuando": "cdo", "nada": "nd"}


def add_noise(text, rng, level=1.0):
    t = text.lower()
    if rng.random() < 0.28 * level:
        t = t.translate(_ACC)
    if rng.random() < 0.40 * level:
        t = t.replace("¿", "").replace("¡", "")
    if rng.random() < 0.35 * level:
        t = re.sub(r"[?!.]+$", "", t)
    elif rng.random() < 0.06 * level and t and t[-1] in "?!":
        t = t + t[-1]
    if rng.random() < 0.14 * level:
        words = t.split(" ")
        for i, w in enumerate(words):
            core = re.sub(r"[^\wáéíóúüñ]", "", w)
            if core in _ABBR and rng.random() < 0.6:
                words[i] = w.replace(core, _ABBR[core])
        t = " ".join(words)
    if rng.random() < 0.05 * level:
        words = t.split(" ")
        cand = [i for i, w in enumerate(words) if len(w) >= 5 and w.isalpha()]
        if cand:
            i = rng.choice(cand)
            w = words[i]
            j = rng.randrange(1, len(w) - 1)
            words[i] = (w[:j] + w[j + 1] + w[j] + w[j + 2:]) if rng.random() < 0.6 else (w[:j] + w[j + 1:])
            t = " ".join(words)
    if rng.random() < 0.04 * level:
        t = re.sub(r"\b(hola|bien|gracias|buenas)\b", lambda m: m.group(1) + m.group(1)[-1] * rng.choice([1, 2, 3]), t, count=1)
    return t.strip() or text.lower()


_PRE = ["che ", "ey ", "mirá, ", "una pregunta: ", "oye ", "disculpá, ", "bueno, ", "a ver, ", "dime, ", "decime, "]
_POST = [" porfa", " jaja", " por favor", " :)", ", ¿sí?", " che", " nomás"]


def add_filler(text, rng):
    r = rng.random()
    if r < 0.07:
        return rng.choice(_PRE) + text
    if r < 0.12:
        return text + rng.choice(_POST)
    return text
