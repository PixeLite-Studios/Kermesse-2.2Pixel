"""Bloque 4: base de conocimiento verificada (capitales, ciencia, geografía...), trivia, cuentas y traducciones."""
from datagen.lex import I


def kb(name, qs, ans, w=1):
    return I(name, qs, ans if isinstance(ans, list) else [ans], w=w, tag="kb")


# ====================================================================== capitales
CAPITALS = [
    ("Argentina", "Buenos Aires"), ("Uruguay", "Montevideo"), ("Chile", "Santiago"), ("Perú", "Lima"), ("Paraguay", "Asunción"), ("Brasil", "Brasilia"),
    ("Colombia", "Bogotá"), ("Venezuela", "Caracas"), ("Ecuador", "Quito"), ("México", "Ciudad de México"), ("Cuba", "La Habana"), ("Panamá", "Ciudad de Panamá"),
    ("Costa Rica", "San José"), ("Nicaragua", "Managua"), ("Honduras", "Tegucigalpa"), ("El Salvador", "San Salvador"), ("Guatemala", "Ciudad de Guatemala"),
    ("República Dominicana", "Santo Domingo"), ("España", "Madrid"), ("Portugal", "Lisboa"), ("Francia", "París"), ("Italia", "Roma"), ("Alemania", "Berlín"),
    ("Reino Unido", "Londres"), ("Estados Unidos", "Washington D. C."), ("Canadá", "Ottawa"), ("Japón", "Tokio"), ("China", "Pekín"), ("Rusia", "Moscú"),
    ("Egipto", "El Cairo"), ("Australia", "Canberra"), ("India", "Nueva Delhi"), ("Grecia", "Atenas"), ("Irlanda", "Dublín"), ("Turquía", "Ankara"),
    ("Suiza", "Berna"), ("Austria", "Viena"), ("Suecia", "Estocolmo"), ("Noruega", "Oslo"), ("Países Bajos", "Ámsterdam"), ("Bélgica", "Bruselas"),
    ("Corea del Sur", "Seúl"), ("Nueva Zelanda", "Wellington"), ("Marruecos", "Rabat"), ("Kenia", "Nairobi"), ("Polonia", "Varsovia"), ("Hungría", "Budapest"),
    ("Finlandia", "Helsinki"), ("Dinamarca", "Copenhague"),
]
UNKNOWN_CAPITALS = ["Mongolia", "Kazajistán", "Nepal", "Laos", "Eslovenia", "Burkina Faso", "Madagascar", "Bután", "Letonia", "Camerún", "Uzbekistán", "Zambia",
                    "Malta", "Albania", "Namibia", "Senegal", "Sri Lanka", "Jordania", "Omán", "Fiyi", "Moldavia", "Tayikistán", "Surinam", "Gabón", "Botsuana"]
CAP_Q = ["¿cuál es la capital de {c}?", "capital de {c}", "¿cuál es la capital de {c}?", "¿sabés la capital de {c}?", "decime la capital de {c}", "¿cómo se llama la capital de {c}?",
         "¿cuál es la ciudad capital de {c}?", "capital de {c}?", "¿cuál es la capital de {c}, kermesse?", "¿cuál era la capital de {c}?", "¿sabes cuál es la capital de {c}?", "¿y la capital de {c}?"]
CAP_A = ["La capital de {c} es {k}.", "La capital de {c} es {k}.", "{k} es la capital de {c}.", "La capital de {c} es {k}. ¿Querés que te pregunte otra?", "Es {k}, la capital de {c}.", "La capital de {c} es {k}. ¿Otra?"]
CAP_REV = ["¿de qué país es capital {k}?", "¿{k} es la capital de qué país?", "¿de qué país es capital {k}?"]
CAP_REV_A = ["{k} es la capital de {c}.", "{k} es la capital de {c}. ¿Querés saber otra?"]
CAP_UNK_A = ["Esa capital no me la sé, perdón. Prefiero no inventar. ¿Probamos con otro país?", "Uf, de {c} no me acuerdo la capital. No quiero decirte algo equivocado. ¿Otro país?", "No sé cuál es la capital de {c}. Soy chiquita y me falta mucho por aprender. ¿Intentamos con otra?"]


def gen_capital(rng):
    r = rng.random()
    if r < 0.08:
        return [(rng.choice(CAP_Q).format(c="Bolivia"), rng.choice(["Bolivia tiene dos capitales: Sucre, la capital constitucional, y La Paz, sede del gobierno.", "En Bolivia son dos: Sucre es la capital constitucional y La Paz es la sede del gobierno."]))]
    if r < 0.25:
        c = rng.choice(UNKNOWN_CAPITALS)
        return [(rng.choice(CAP_Q).format(c=c), rng.choice(CAP_UNK_A).format(c=c))]
    c, k = rng.choice(CAPITALS)
    if r < 0.37:
        return [(rng.choice(CAP_REV).format(k=k), rng.choice(CAP_REV_A).format(k=k, c=c))]
    return [(rng.choice(CAP_Q).format(c=c), rng.choice(CAP_A).format(c=c, k=k))]


# ====================================================================== cuentas
def _fmt_q(rng, a, b, op):
    if op == "+":
        t = ["¿cuánto es {a} + {b}?", "{a}+{b}", "cuánto es {a} más {b}", "¿cuánto es {a} más {b}?", "sumá {a} y {b}", "{a} más {b}", "¿cuánto da {a} más {b}?", "{a} + {b}", "¿cuánto es {a}+{b}?", "cuánto da {a} + {b}", "suma {a} más {b}"]
    elif op == "-":
        t = ["¿cuánto es {a} - {b}?", "{a}-{b}", "cuánto es {a} menos {b}", "¿cuánto es {a} menos {b}?", "restá {b} a {a}", "{a} menos {b}", "¿cuánto da {a} menos {b}?", "{a} - {b}", "¿cuánto es {a}-{b}?", "cuánto da {a} - {b}"]
    elif op == "*":
        t = ["¿cuánto es {a} x {b}?", "{a}x{b}", "cuánto es {a} por {b}", "¿cuánto es {a} por {b}?", "multiplicá {a} por {b}", "{a} por {b}", "¿cuánto da {a} por {b}?", "{a} * {b}", "¿cuánto es {a}x{b}?", "cuánto da {a} x {b}"]
    else:
        t = ["¿cuánto es {a} / {b}?", "{a}/{b}", "cuánto es {a} dividido {b}", "¿cuánto es {a} dividido {b}?", "dividí {a} por {b}", "{a} dividido {b}", "¿cuánto da {a} dividido {b}?", "{a} / {b}", "¿cuánto es {a}:{b}?", "cuánto da {a} / {b}"]
    return rng.choice(t).format(a=a, b=b)


_NAME = {"+": "más", "-": "menos", "*": "por", "/": "dividido"}
_SYM = {"+": "+", "-": "-", "*": "x", "/": "/"}


def gen_math(rng):
    op = rng.choice(["+", "+", "-", "-", "*", "*", "/"])
    if op == "+":
        hi = 20 if rng.random() < 0.4 else 50
        a, b = rng.randint(0, hi), rng.randint(0, hi); r = a + b
    elif op == "-":
        hi = 20 if rng.random() < 0.4 else 50
        a, b = rng.randint(0, hi), rng.randint(0, hi)
        if b > a:
            a, b = b, a
        r = a - b
    elif op == "*":
        a, b = rng.randint(0, 10), rng.randint(0, 10); r = a * b
    else:
        b = rng.randint(1, 10); c = rng.randint(0, 10); a = b * c; r = c
    q = _fmt_q(rng, a, b, op)
    ans = rng.choice(["{a} {n} {b} es {r}.", "{a} {s} {b} = {r}.", "Son {r}." if False else "El resultado es {r}.", "{a} {n} {b} da {r}.", "Da {r}.", "{a} {n} {b} es {r}. ¿Querés otra cuenta?", "Es {r}."]).format(a=a, b=b, r=r, n=_NAME[op], s=_SYM[op])
    return [(q, ans)]


def gen_math_extra(rng):
    k = rng.random()
    if k < 0.3:
        n = rng.randint(1, 30)
        return [(rng.choice(["¿cuál es el doble de {n}?", "el doble de {n}", "doble de {n}", "¿cuánto es el doble de {n}?"]).format(n=n), rng.choice(["El doble de {n} es {r}.", "Es {r}. El doble de {n}."]).format(n=n, r=2 * n))]
    if k < 0.55:
        n = 2 * rng.randint(1, 30)
        return [(rng.choice(["¿cuál es la mitad de {n}?", "la mitad de {n}", "mitad de {n}", "¿cuánto es la mitad de {n}?"]).format(n=n), rng.choice(["La mitad de {n} es {r}.", "Es {r}. La mitad de {n}."]).format(n=n, r=n // 2))]
    if k < 0.75:
        n = rng.randint(1, 12)
        return [(rng.choice(["¿cuánto es {n} al cuadrado?", "{n} al cuadrado", "¿cuál es el cuadrado de {n}?"]).format(n=n), rng.choice(["{n} al cuadrado es {r}.", "El cuadrado de {n} es {r}."]).format(n=n, r=n * n))]
    if k < 0.9:
        n = rng.randint(1, 12)
        return [(rng.choice(["¿cuál es la raíz cuadrada de {s}?", "raíz de {s}", "raíz cuadrada de {s}", "¿cuánto es la raíz de {s}?"]).format(s=n * n), rng.choice(["La raíz cuadrada de {s} es {n}.", "Es {n}, porque {n} por {n} es {s}."]).format(s=n * n, n=n))]
    n = rng.randint(2, 9)
    return [(rng.choice(["contame de {n} en {n} hasta {t}", "contá de {n} en {n}", "tabla del {n}"]).format(n=n, t=n * 6),
             "Ahí va: " + ", ".join(str(n * i) for i in range(1, 7)) + ".")]


# ====================================================================== calendario
DAYS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
MDAYS = {"enero": 31, "febrero": 28, "marzo": 31, "abril": 30, "mayo": 31, "junio": 30, "julio": 31, "agosto": 31, "septiembre": 30, "octubre": 31, "noviembre": 30, "diciembre": 31}


def gen_calendar(rng):
    k = rng.random()
    if k < 0.3:
        d = rng.choice(DAYS); n = DAYS[(DAYS.index(d) + 1) % 7]
        return [(rng.choice(["¿qué día viene después del {d}?", "¿qué día es después del {d}?", "después del {d}, ¿qué día sigue?", "¿qué día sigue al {d}?"]).format(d=d), "Después del {d} viene el {n}.".format(d=d, n=n))]
    if k < 0.45:
        d = rng.choice(DAYS); p = DAYS[(DAYS.index(d) - 1) % 7]
        return [(rng.choice(["¿qué día viene antes del {d}?", "¿qué día es antes del {d}?", "¿qué día va antes del {d}?"]).format(d=d), "Antes del {d} viene el {p}.".format(d=d, p=p))]
    if k < 0.7:
        m = rng.choice(MONTHS); n = MONTHS[(MONTHS.index(m) + 1) % 12]
        return [(rng.choice(["¿qué mes viene después de {m}?", "¿qué mes sigue a {m}?", "después de {m}, ¿qué mes viene?", "¿qué mes es después de {m}?"]).format(m=m), "Después de {m} viene {n}.".format(m=m, n=n))]
    if k < 0.82:
        m = rng.choice(MONTHS); p = MONTHS[(MONTHS.index(m) - 1) % 12]
        return [(rng.choice(["¿qué mes viene antes de {m}?", "¿qué mes es antes de {m}?"]).format(m=m), "Antes de {m} viene {p}.".format(m=m, p=p))]
    m = rng.choice(MONTHS)
    q = rng.choice(["¿cuántos días tiene {m}?", "¿cuántos días tiene el mes de {m}?", "días de {m}?"]).format(m=m)
    if m == "febrero":
        return [(q, "Febrero tiene 28 días, y 29 en los años bisiestos.")]
    return [(q, rng.choice(["{M} tiene {n} días.", "El mes de {m} tiene {n} días."]).format(M=m.capitalize(), m=m, n=MDAYS[m]))]


# ====================================================================== traducciones
TR = {
    "inglés": [("hola", "hello"), ("adiós", "goodbye"), ("gracias", "thank you"), ("por favor", "please"), ("buenos días", "good morning"), ("buenas noches", "good night"), ("te quiero", "I love you"),
               ("agua", "water"), ("casa", "house"), ("perro", "dog"), ("gato", "cat"), ("amigo", "friend"), ("comida", "food"), ("libro", "book"), ("sol", "sun"), ("luna", "moon"), ("mesa", "table"),
               ("rojo", "red"), ("azul", "blue"), ("verde", "green"), ("uno", "one"), ("dos", "two"), ("tres", "three"), ("manzana", "apple"), ("leche", "milk"), ("pan", "bread"), ("feliz", "happy"),
               ("triste", "sad"), ("escuela", "school"), ("familia", "family"), ("ventana", "window"), ("noche", "night"), ("día", "day")],
    "francés": [("hola", "bonjour"), ("gracias", "merci"), ("adiós", "au revoir"), ("buenas noches", "bonne nuit"), ("agua", "eau"), ("amigo", "ami"), ("pan", "pain"), ("gato", "chat"), ("perro", "chien"), ("libro", "livre")],
    "italiano": [("hola", "ciao"), ("gracias", "grazie"), ("buenos días", "buongiorno"), ("adiós", "arrivederci"), ("agua", "acqua"), ("amigo", "amico"), ("gato", "gatto"), ("casa", "casa")],
    "portugués": [("hola", "olá"), ("gracias", "obrigado"), ("buenos días", "bom dia"), ("adiós", "tchau"), ("agua", "água"), ("gato", "gato"), ("libro", "livro"), ("amigo", "amigo")],
}


def gen_translate(rng):
    lang = rng.choices(list(TR), weights=[6, 1, 1, 1])[0]
    es, x = rng.choice(TR[lang])
    if rng.random() < 0.7:
        q = rng.choice(["¿cómo se dice {es} en {l}?", "{es} en {l}", "¿cómo se dice '{es}' en {l}?".replace("'", ""), "traducí {es} al {l}", "¿cómo digo {es} en {l}?", "decime {es} en {l}"]).format(es=es, l=lang) if lang != "inglés" else \
            rng.choice(["¿cómo se dice {es} en inglés?", "{es} en inglés", "traducí {es} al inglés", "¿cómo digo {es} en inglés?", "decime {es} en inglés", "¿cómo se dice {es} en inglés, kermesse?"]).format(es=es)
        q = q.replace("al inglés", "al inglés").replace("al francés", "al francés")
        a = rng.choice(["En {l}, {es} se dice {x}.", "{es} se dice {x} en {l}.", "Se dice {x}. ¿Querés otra palabra?"]).format(es=es.capitalize() if False else es, x=x, l=lang)
        a = a[0].upper() + a[1:] if a[0].islower() else a
        return [(q, a)]
    q = rng.choice(["¿qué significa {x}?", "¿cómo se dice {x} en español?", "{x} en español", "¿qué quiere decir {x}?", "traducí {x} al español"]).format(x=x.lower())
    a = rng.choice(["{x} significa {es}.", "En español, {x} es {es}.", "{x} quiere decir {es}."]).format(x=x[0].upper() + x[1:], es=es)
    return [(q, a)]


# ====================================================================== intents de conocimiento (hechos fijos)
INTENTS = [
    kb("planetas_cuantos", ["¿cuántos planetas hay?", "¿cuántos planetas tiene el sistema solar?", "¿cuántos planetas hay en el sistema solar?", "cantidad de planetas", "¿cuáles son los planetas?", "nombrame los planetas", "decime los planetas del sistema solar", "planetas del sistema solar"],
       ["El sistema solar tiene ocho planetas: Mercurio, Venus, Tierra, Marte, Júpiter, Saturno, Urano y Neptuno.", "Son ocho: Mercurio, Venus, la Tierra, Marte, Júpiter, Saturno, Urano y Neptuno. ¿Cuál te gusta más?"]),
    kb("planeta_grande", ["¿cuál es el planeta más grande?", "¿cuál es el planeta más grande del sistema solar?", "planeta más grande", "¿cuál es el planeta más grande que existe?"], ["El planeta más grande del sistema solar es Júpiter.", "Júpiter es el más grande de todos. ¿Sabías que cabrían más de mil Tierras adentro?"]),
    kb("planeta_chico", ["¿cuál es el planeta más pequeño?", "planeta más chico", "¿cuál es el planeta más chico del sistema solar?"], ["El planeta más pequeño del sistema solar es Mercurio."]),
    kb("planeta_cerca", ["¿cuál es el planeta más cercano al sol?", "planeta más cercano al sol", "¿qué planeta está más cerca del sol?"], ["El planeta más cercano al Sol es Mercurio."]),
    kb("planeta_rojo", ["¿cuál es el planeta rojo?", "¿qué planeta es rojo?", "planeta rojo", "¿cuál es el planeta de color rojo?"], ["El planeta rojo es Marte, por el óxido de hierro de su superficie."]),
    kb("planeta_anillos", ["¿qué planeta tiene anillos?", "¿cuál es el planeta de los anillos?", "planeta con anillos", "¿qué planeta es famoso por sus anillos?"], ["Saturno es el planeta famoso por sus anillos."]),
    kb("planeta_caliente", ["¿cuál es el planeta más caliente?", "planeta más caliente", "¿qué planeta es el más caluroso?"], ["El planeta más caliente es Venus, por su atmósfera que atrapa el calor."]),
    kb("planeta_casa", ["¿en qué planeta vivimos?", "¿cómo se llama nuestro planeta?", "¿en qué planeta estamos?", "¿cuál es nuestro planeta?"], ["Vivimos en la Tierra, el tercer planeta contando desde el Sol."]),
    kb("sol_que", ["¿qué es el sol?", "¿el sol es un planeta?", "¿el sol es una estrella?", "¿qué es el sol, un planeta?"], ["El Sol es una estrella, la más cercana a la Tierra. Nos da luz y calor."]),
    kb("luna_que", ["¿qué es la luna?", "¿cuántas lunas tiene la tierra?", "¿la luna es un planeta?", "¿la tierra tiene luna?"], ["La Luna es el satélite natural de la Tierra. Tenemos una sola."]),
    kb("galaxia", ["¿cómo se llama nuestra galaxia?", "¿en qué galaxia vivimos?", "¿cuál es nuestra galaxia?", "¿qué galaxia es la nuestra?"], ["Nuestra galaxia se llama la Vía Láctea."]),
    kb("pluton", ["¿plutón es un planeta?", "¿qué pasó con plutón?", "¿es plutón un planeta?", "¿plutón sigue siendo un planeta?"], ["Plutón es un planeta enano: dejó de considerarse planeta en 2006."]),
    kb("animal_grande", ["¿cuál es el animal más grande?", "animal más grande del mundo", "¿cuál es el animal más grande del planeta?", "¿cuál es el animal más grande que existe?"], ["El animal más grande del mundo es la ballena azul."]),
    kb("animal_rapido", ["¿cuál es el animal más rápido?", "animal más rápido", "¿cuál es el animal terrestre más rápido?", "¿qué animal corre más rápido?"], ["El animal terrestre más rápido es el guepardo."]),
    kb("animal_alto", ["¿cuál es el animal más alto?", "animal más alto", "¿qué animal es el más alto?"], ["El animal más alto del mundo es la jirafa."]),
    kb("araña_patas", ["¿cuántas patas tiene una araña?", "patas de una araña", "¿cuántas patas tienen las arañas?"], ["Las arañas tienen ocho patas."]),
    kb("insecto_patas", ["¿cuántas patas tiene un insecto?", "patas de un insecto", "¿cuántas patas tienen los insectos?"], ["Los insectos tienen seis patas."]),
    kb("ave_no_vuela", ["¿qué ave no vuela?", "nombrá un ave que no vuele", "¿qué aves no pueden volar?", "ave que no vuela"], ["El pingüino y el avestruz son aves que no vuelan."]),
    kb("canguro", ["¿dónde viven los canguros?", "¿de qué país son los canguros?", "¿dónde viven los koalas?", "¿de dónde son los koalas?"], ["Los canguros y los koalas viven en Australia."]),
    kb("panda", ["¿qué come el panda?", "¿de qué se alimenta el oso panda?", "¿qué comen los pandas?"], ["El oso panda se alimenta sobre todo de bambú."]),
    kb("vaca_sonido", ["¿qué sonido hace la vaca?", "¿cómo hace la vaca?", "sonido de la vaca"], ["La vaca hace muuu: mugir se llama su sonido."]),
    kb("perro_sonido", ["¿qué sonido hace el perro?", "¿cómo hace el perro?", "sonido del perro"], ["El perro ladra: guau, guau."]),
    kb("gato_sonido", ["¿qué sonido hace el gato?", "¿cómo hace el gato?", "sonido del gato"], ["El gato maúlla: miau, miau."]),
    kb("caballo_sonido", ["¿qué sonido hace el caballo?", "¿cómo hace el caballo?"], ["El caballo relincha."]),
    kb("pato_sonido", ["¿qué sonido hace el pato?", "¿cómo hace el pato?"], ["El pato hace cuac, cuac."]),
    kb("leon", ["¿cómo se llama el rey de la selva?", "¿quién es el rey de la selva?", "¿qué sonido hace el león?"], ["El león es llamado el rey de la selva, y su sonido es el rugido."]),
    kb("mamifero", ["¿qué es un mamífero?", "¿qué animales son mamíferos?", "¿qué significa mamífero?"], ["Un mamífero es un animal que amamanta a sus crías, como los perros, las ballenas y las personas."]),
    kb("huesos", ["¿cuántos huesos tiene el cuerpo humano?", "¿cuántos huesos tenemos?", "huesos del cuerpo humano", "¿cuántos huesos tiene un adulto?"], ["Un adulto tiene 206 huesos."]),
    kb("corazon", ["¿para qué sirve el corazón?", "¿qué hace el corazón?", "¿cuál es la función del corazón?"], ["El corazón bombea la sangre por todo el cuerpo."]),
    kb("dientes", ["¿cuántos dientes tiene un adulto?", "¿cuántos dientes tenemos?", "dientes de un adulto"], ["Un adulto tiene 32 dientes."]),
    kb("sentidos", ["¿cuántos sentidos tenemos?", "¿cuáles son los cinco sentidos?", "nombrá los sentidos", "los sentidos del cuerpo"], ["Tenemos cinco sentidos: vista, oído, olfato, gusto y tacto."]),
    kb("pulmones", ["¿qué órgano usamos para respirar?", "¿para qué sirven los pulmones?", "¿con qué respiramos?"], ["Respiramos con los pulmones."]),
    kb("organo_grande", ["¿cuál es el órgano más grande del cuerpo?", "órgano más grande"], ["El órgano más grande del cuerpo es la piel."]),
    kb("agua_hierve", ["¿a qué temperatura hierve el agua?", "¿cuándo hierve el agua?", "temperatura de ebullición del agua"], ["El agua hierve a 100 grados, al nivel del mar."]),
    kb("agua_congela", ["¿a qué temperatura se congela el agua?", "¿cuándo se congela el agua?", "temperatura de congelación del agua"], ["El agua se congela a 0 grados."]),
    kb("agua_formula", ["¿cuál es la fórmula del agua?", "fórmula del agua", "¿de qué está hecha el agua?", "¿cómo se escribe el agua químicamente?"], ["La fórmula del agua es H2O: dos átomos de hidrógeno y uno de oxígeno."]),
    kb("gravedad", ["¿qué es la gravedad?", "¿por qué caen las cosas?", "explicame la gravedad"], ["La gravedad es la fuerza que atrae los objetos hacia la Tierra, por eso las cosas caen."]),
    kb("fotosintesis", ["¿qué es la fotosíntesis?", "¿cómo se alimentan las plantas?", "explicame la fotosíntesis", "¿cómo hacen su comida las plantas?"], ["Con la fotosíntesis, las plantas usan luz del Sol, agua y aire para fabricar su alimento."]),
    kb("plantas_necesitan", ["¿qué necesitan las plantas para vivir?", "¿qué necesita una planta para crecer?"], ["Las plantas necesitan agua, luz y aire."]),
    kb("estados_materia", ["¿cuáles son los estados de la materia?", "estados de la materia", "¿cuáles son los estados del agua?"], ["Los estados de la materia son sólido, líquido y gaseoso."]),
    kb("arcoiris", ["¿cuántos colores tiene el arcoíris?", "colores del arcoíris", "¿de qué colores es el arcoíris?"], ["El arcoíris tiene siete colores: rojo, naranja, amarillo, verde, celeste, azul y violeta."]),
    kb("mezcla_verde", ["¿qué colores mezclo para hacer verde?", "¿cómo se hace el verde?", "azul más amarillo", "¿qué da azul con amarillo?"], ["Azul más amarillo da verde."]),
    kb("mezcla_naranja", ["¿qué colores mezclo para hacer naranja?", "¿cómo se hace el naranja?", "rojo más amarillo", "¿qué da rojo con amarillo?"], ["Rojo más amarillo da naranja."]),
    kb("mezcla_violeta", ["¿qué colores mezclo para hacer violeta?", "¿cómo se hace el violeta?", "rojo más azul", "¿qué da rojo con azul?"], ["Rojo más azul da violeta, mi color favorito."]),
    kb("mezcla_rosa", ["¿cómo se hace el rosa?", "rojo más blanco", "¿qué da rojo con blanco?"], ["Rojo más blanco da rosa."]),
    kb("mezcla_gris", ["¿cómo se hace el gris?", "blanco más negro", "¿qué da blanco con negro?"], ["Blanco más negro da gris."]),
    kb("dias_semana", ["¿cuántos días tiene una semana?", "¿cuáles son los días de la semana?", "días de la semana", "nombrá los días de la semana"], ["La semana tiene siete días: lunes, martes, miércoles, jueves, viernes, sábado y domingo."]),
    kb("meses", ["¿cuántos meses tiene un año?", "¿cuáles son los meses del año?", "meses del año", "nombrá los meses"], ["El año tiene doce meses: enero, febrero, marzo, abril, mayo, junio, julio, agosto, septiembre, octubre, noviembre y diciembre."]),
    kb("dias_año", ["¿cuántos días tiene un año?", "días del año", "¿cuántos días tiene el año?"], ["Un año tiene 365 días, y 366 cuando es bisiesto."]),
    kb("bisiesto", ["¿qué es un año bisiesto?", "¿cada cuánto hay año bisiesto?", "año bisiesto"], ["Un año bisiesto tiene 366 días y ocurre cada cuatro años. Febrero suma un día."]),
    kb("horas_dia", ["¿cuántas horas tiene un día?", "horas de un día", "¿cuántas horas tiene el día?"], ["Un día tiene 24 horas."]),
    kb("minutos_hora", ["¿cuántos minutos tiene una hora?", "minutos de una hora", "¿cuántos minutos hay en una hora?"], ["Una hora tiene 60 minutos."]),
    kb("segundos_min", ["¿cuántos segundos tiene un minuto?", "segundos de un minuto", "¿cuántos segundos hay en un minuto?"], ["Un minuto tiene 60 segundos."]),
    kb("siglo", ["¿cuántos años tiene un siglo?", "años de un siglo", "¿cuántos años son un siglo?"], ["Un siglo tiene 100 años."]),
    kb("decada", ["¿cuántos años tiene una década?", "años de una década", "¿cuántos años son una década?"], ["Una década tiene 10 años."]),
    kb("estaciones", ["¿cuáles son las estaciones del año?", "estaciones del año", "¿cuántas estaciones hay?"], ["Las estaciones son cuatro: primavera, verano, otoño e invierno."]),
    kb("docena", ["¿cuánto es una docena?", "¿cuántos son una docena?", "¿cuántas unidades tiene una docena?"], ["Una docena son 12 unidades."]),
    kb("lados_triangulo", ["¿cuántos lados tiene un triángulo?", "lados de un triángulo"], ["Un triángulo tiene tres lados."]),
    kb("lados_cuadrado", ["¿cuántos lados tiene un cuadrado?", "lados de un cuadrado"], ["Un cuadrado tiene cuatro lados iguales."]),
    kb("lados_hexagono", ["¿cuántos lados tiene un hexágono?", "lados de un hexágono"], ["Un hexágono tiene seis lados."]),
    kb("angulo_recto", ["¿cuántos grados tiene un ángulo recto?", "ángulo recto", "¿cuánto mide un ángulo recto?"], ["Un ángulo recto mide 90 grados."]),
    kb("pi", ["¿qué es pi?", "¿cuánto vale pi?", "número pi", "¿cuál es el valor de pi?"], ["Pi es un número que vale aproximadamente 3,14. Sale de dividir la longitud de una circunferencia por su diámetro."]),
    kb("primos", ["¿qué es un número primo?", "números primos", "dame números primos", "nombrá algunos números primos"], ["Un número primo solo se divide por 1 y por sí mismo. Por ejemplo: 2, 3, 5, 7 y 11."]),
    kb("par_impar", ["¿qué es un número par?", "¿qué es un número impar?", "número par", "número impar"], ["Un número par se puede dividir en dos partes iguales, como el 2, el 4 o el 6. Los impares, como el 1, el 3 o el 5, no."]),
    kb("continentes", ["¿cuántos continentes hay?", "¿cuáles son los continentes?", "continentes del mundo", "nombrá los continentes"], ["Hay seis o siete, según cómo se cuenten: África, América, Antártida, Asia, Europa y Oceanía."]),
    kb("oceanos", ["¿cuántos océanos hay?", "¿cuáles son los océanos?", "océanos del mundo"], ["Hay cinco océanos: Pacífico, Atlántico, Índico, Antártico y Ártico."]),
    kb("oceano_grande", ["¿cuál es el océano más grande?", "océano más grande", "¿cuál es el océano más extenso?"], ["El océano más grande es el Pacífico."]),
    kb("rio_largo", ["¿cuál es el río más largo del mundo?", "río más largo", "¿cuál es el río más caudaloso?"], ["Se discute entre el Nilo y el Amazonas: suele decirse que el Nilo es más largo, pero el Amazonas es el más caudaloso."]),
    kb("montana_alta", ["¿cuál es la montaña más alta del mundo?", "montaña más alta", "¿cuál es la montaña más alta de la tierra?", "¿cuál es el pico más alto del mundo?"], ["La montaña más alta del mundo es el Everest, en la cordillera del Himalaya."]),
    kb("aconcagua", ["¿cuál es la montaña más alta de américa?", "¿dónde está el aconcagua?", "¿qué es el aconcagua?", "montaña más alta de américa"], ["El Aconcagua, en Argentina, es la montaña más alta de América."]),
    kb("pais_grande", ["¿cuál es el país más grande del mundo?", "país más grande", "¿cuál es el país más extenso?"], ["El país más grande del mundo es Rusia."]),
    kb("pais_chico", ["¿cuál es el país más pequeño del mundo?", "país más pequeño", "¿cuál es el país más chico?"], ["El país más pequeño del mundo es la Ciudad del Vaticano."]),
    kb("desierto", ["¿cuál es el desierto más grande?", "desierto más grande", "¿dónde está el sahara?", "¿qué es el sahara?"], ["El Sahara, en África, es el desierto cálido más grande del mundo."]),
    kb("machu", ["¿dónde está machu picchu?", "¿en qué país está machu picchu?", "machu picchu"], ["Machu Picchu está en Perú, cerca de Cusco."]),
    kb("piramides", ["¿dónde están las pirámides de giza?", "¿en qué país están las pirámides?", "pirámides de giza"], ["Las pirámides de Giza están en Egipto."]),
    kb("eiffel", ["¿dónde está la torre eiffel?", "¿en qué ciudad está la torre eiffel?", "torre eiffel"], ["La torre Eiffel está en París, Francia."]),
    kb("coliseo", ["¿dónde está el coliseo?", "¿en qué ciudad está el coliseo romano?", "coliseo romano"], ["El Coliseo está en Roma, Italia."]),
    kb("cristo", ["¿dónde está el cristo redentor?", "cristo redentor", "¿en qué ciudad está el cristo redentor?"], ["El Cristo Redentor está en Río de Janeiro, Brasil."]),
    kb("chichen", ["¿dónde está chichén itzá?", "chichén itzá", "¿en qué país está chichén itzá?"], ["Chichén Itzá está en México, en la península de Yucatán."]),
    kb("iguazu", ["¿dónde están las cataratas del iguazú?", "cataratas del iguazú", "¿en qué país están las cataratas del iguazú?"], ["Las cataratas del Iguazú están entre Argentina y Brasil."]),
    kb("muralla", ["¿dónde está la gran muralla?", "gran muralla china", "¿en qué país está la gran muralla?"], ["La Gran Muralla está en China."]),
    kb("libertad", ["¿dónde está la estatua de la libertad?", "estatua de la libertad", "¿en qué ciudad está la estatua de la libertad?"], ["La Estatua de la Libertad está en Nueva York, Estados Unidos."]),
    kb("taj", ["¿dónde está el taj mahal?", "taj mahal", "¿en qué país está el taj mahal?"], ["El Taj Mahal está en India."]),
    kb("bigben", ["¿dónde está el big ben?", "big ben", "¿en qué ciudad está el big ben?"], ["El Big Ben está en Londres, Reino Unido."]),
    kb("sagrada", ["¿dónde está la sagrada familia?", "sagrada familia", "¿en qué ciudad está la sagrada familia?"], ["La Sagrada Familia está en Barcelona, España."]),
    kb("uyuni", ["¿dónde está el salar de uyuni?", "salar de uyuni", "¿en qué país está el salar de uyuni?"], ["El salar de Uyuni está en Bolivia."]),
    kb("galapagos", ["¿dónde están las islas galápagos?", "islas galápagos", "¿en qué país están las galápagos?"], ["Las islas Galápagos pertenecen a Ecuador."]),
    kb("titicaca", ["¿dónde está el lago titicaca?", "lago titicaca", "¿en qué país está el lago titicaca?"], ["El lago Titicaca está entre Perú y Bolivia."]),
    kb("quijote", ["¿quién escribió don quijote?", "¿quién escribió el quijote?", "autor del quijote", "¿quién escribió don quijote de la mancha?"], ["Don Quijote de la Mancha fue escrito por Miguel de Cervantes."]),
    kb("cien_anios", ["¿quién escribió cien años de soledad?", "autor de cien años de soledad", "¿quién es gabriel garcía márquez?"], ["Cien años de soledad lo escribió Gabriel García Márquez, un escritor colombiano."]),
    kb("mona_lisa", ["¿quién pintó la mona lisa?", "autor de la mona lisa", "¿quién hizo la gioconda?"], ["La Mona Lisa fue pintada por Leonardo da Vinci."]),
    kb("guernica", ["¿quién pintó el guernica?", "autor del guernica", "¿quién es picasso?"], ["El Guernica lo pintó Pablo Picasso."]),
    kb("noche_estrellada", ["¿quién pintó la noche estrellada?", "autor de la noche estrellada", "¿quién es van gogh?"], ["La noche estrellada es de Vincent van Gogh."]),
    kb("martin_fierro", ["¿quién escribió martín fierro?", "autor de martín fierro"], ["Martín Fierro fue escrito por José Hernández."]),
    kb("rayuela", ["¿quién escribió rayuela?", "autor de rayuela", "¿quién es cortázar?"], ["Rayuela es de Julio Cortázar, un escritor argentino."]),
    kb("borges", ["¿quién es borges?", "¿quién fue jorge luis borges?"], ["Jorge Luis Borges fue un escritor argentino famoso por sus cuentos, como El Aleph."]),
    kb("neruda", ["¿quién es pablo neruda?", "¿quién fue neruda?"], ["Pablo Neruda fue un poeta chileno que ganó el Premio Nobel de Literatura."]),
    kb("frida", ["¿quién es frida kahlo?", "¿quién fue frida kahlo?"], ["Frida Kahlo fue una pintora mexicana famosa por sus autorretratos."]),
    kb("beethoven", ["¿quién fue beethoven?", "¿quién es beethoven?", "¿quién compuso la novena sinfonía?"], ["Ludwig van Beethoven fue un compositor alemán. Siguió componiendo aun cuando perdió la audición."]),
    kb("mozart", ["¿quién fue mozart?", "¿quién es mozart?"], ["Wolfgang Amadeus Mozart fue un compositor austríaco que empezó a componer de niño."]),
    kb("mafalda", ["¿quién creó a mafalda?", "¿quién es mafalda?", "¿quién dibujó mafalda?"], ["Mafalda es un personaje de historieta creado por Quino, un dibujante argentino."]),
    kb("futbol_jugadores", ["¿cuántos jugadores hay en un equipo de fútbol?", "jugadores de fútbol por equipo", "¿cuántos juegan al fútbol?", "¿cuántos jugadores tiene un equipo de fútbol?"], ["Cada equipo de fútbol juega con once jugadores en la cancha."]),
    kb("futbol_tiempo", ["¿cuánto dura un partido de fútbol?", "duración de un partido de fútbol"], ["Un partido de fútbol dura 90 minutos, dos tiempos de 45."]),
    kb("basquet_jugadores", ["¿cuántos jugadores hay en un equipo de básquet?", "jugadores de básquet por equipo"], ["Cada equipo de básquet tiene cinco jugadores en la cancha."]),
    kb("idioma_hablan", ["¿cuánta gente habla español?", "¿cuántas personas hablan español?", "¿en cuántos países se habla español?"], ["El español lo hablan cerca de quinientos millones de personas en todo el mundo."]),
    kb("cacao", ["¿de dónde sale el chocolate?", "¿de qué se hace el chocolate?", "¿qué es el cacao?"], ["El chocolate se hace con cacao, la semilla de un árbol que nació en América."]),
    kb("mate", ["¿qué es el mate?", "¿de qué es el mate?", "¿qué es el mate argentino?"], ["El mate es una infusión de yerba mate, muy típica de Sudamérica, que se comparte en ronda."]),
]

# ====================================================================== TRIVIA (pregunta, respuesta, formas aceptadas, errores plausibles)
TRIVIA = [
    ("¿Cuál es la capital de Perú?", "Lima", ["lima"], ["cusco", "bogotá", "quito"]),
    ("¿Cuál es la capital de Argentina?", "Buenos Aires", ["buenos aires"], ["córdoba", "rosario", "montevideo"]),
    ("¿Cuál es la capital de Chile?", "Santiago", ["santiago"], ["valparaíso", "lima", "mendoza"]),
    ("¿Cuál es la capital de Uruguay?", "Montevideo", ["montevideo"], ["buenos aires", "asunción", "lima"]),
    ("¿Cuál es la capital de Colombia?", "Bogotá", ["bogotá", "bogota"], ["medellín", "cali", "caracas"]),
    ("¿Cuál es la capital de España?", "Madrid", ["madrid"], ["barcelona", "sevilla", "lisboa"]),
    ("¿Cuál es la capital de Francia?", "París", ["parís", "paris"], ["lyon", "marsella", "roma"]),
    ("¿Cuál es la capital de Italia?", "Roma", ["roma"], ["milán", "venecia", "madrid"]),
    ("¿Cuál es la capital de Japón?", "Tokio", ["tokio"], ["kioto", "osaka", "pekín"]),
    ("¿Cuál es la capital de Brasil?", "Brasilia", ["brasilia"], ["río de janeiro", "san pablo", "buenos aires"]),
    ("¿Cuál es la capital de México?", "Ciudad de México", ["ciudad de méxico", "méxico"], ["guadalajara", "cancún", "monterrey"]),
    ("¿Cuál es la capital de Ecuador?", "Quito", ["quito"], ["guayaquil", "lima", "cuenca"]),
    ("¿Cuál es la capital de Alemania?", "Berlín", ["berlín", "berlin"], ["múnich", "hamburgo", "viena"]),
    ("¿Cuál es la capital de Portugal?", "Lisboa", ["lisboa"], ["oporto", "madrid", "faro"]),
    ("¿Cuál es la capital de Canadá?", "Ottawa", ["ottawa"], ["toronto", "montreal", "vancouver"]),
    ("¿Cuál es la capital de Australia?", "Canberra", ["canberra"], ["sídney", "melbourne", "perth"]),
    ("¿Cuál es la capital de Turquía?", "Ankara", ["ankara"], ["estambul", "izmir", "atenas"]),
    ("¿Cuál es el planeta más grande del sistema solar?", "Júpiter", ["júpiter", "jupiter"], ["saturno", "marte", "la tierra"]),
    ("¿Cuál es el planeta rojo?", "Marte", ["marte"], ["venus", "júpiter", "mercurio"]),
    ("¿Cuál es el planeta más cercano al Sol?", "Mercurio", ["mercurio"], ["venus", "marte", "la tierra"]),
    ("¿Qué planeta es famoso por sus anillos?", "Saturno", ["saturno"], ["júpiter", "marte", "urano"]),
    ("¿Cuántos planetas tiene el sistema solar?", "ocho", ["ocho", "8"], ["nueve", "siete", "diez"]),
    ("¿Cuál es el animal más grande del mundo?", "la ballena azul", ["la ballena azul", "ballena azul", "ballena"], ["el elefante", "el tiburón", "la jirafa"]),
    ("¿Cuál es el animal terrestre más rápido?", "el guepardo", ["guepardo", "el guepardo"], ["el león", "el caballo", "el tigre"]),
    ("¿Cuál es el animal más alto?", "la jirafa", ["la jirafa", "jirafa"], ["el elefante", "el camello", "la cebra"]),
    ("¿Cuántas patas tiene una araña?", "ocho", ["ocho", "8"], ["seis", "cuatro", "diez"]),
    ("¿Qué come el oso panda?", "bambú", ["bambú", "bambu"], ["pescado", "miel", "pasto"]),
    ("¿Dónde viven los canguros?", "Australia", ["australia"], ["áfrica", "brasil", "india"]),
    ("¿Cuántos huesos tiene un adulto?", "206", ["206", "doscientos seis"], ["300", "100", "150"]),
    ("¿Cuántos sentidos tenemos?", "cinco", ["cinco", "5"], ["tres", "seis", "cuatro"]),
    ("¿A cuántos grados hierve el agua?", "100", ["100", "cien"], ["50", "0", "200"]),
    ("¿Cuál es la fórmula del agua?", "H2O", ["h2o"], ["co2", "o2", "nacl"]),
    ("¿Cuántos colores tiene el arcoíris?", "siete", ["siete", "7"], ["cinco", "seis", "diez"]),
    ("¿Cuál es el océano más grande?", "el Pacífico", ["pacífico", "el pacífico", "pacifico"], ["el atlántico", "el índico", "el ártico"]),
    ("¿Cuál es la montaña más alta del mundo?", "el Everest", ["everest", "el everest"], ["el aconcagua", "el kilimanjaro", "el mont blanc"]),
    ("¿Cuál es la montaña más alta de América?", "el Aconcagua", ["aconcagua", "el aconcagua"], ["el everest", "el chimborazo", "el fitz roy"]),
    ("¿Cuál es el país más grande del mundo?", "Rusia", ["rusia"], ["china", "canadá", "brasil"]),
    ("¿Dónde está Machu Picchu?", "en Perú", ["perú", "peru", "en perú"], ["en bolivia", "en chile", "en méxico"]),
    ("¿Dónde están las pirámides de Giza?", "en Egipto", ["egipto", "en egipto"], ["en méxico", "en perú", "en grecia"]),
    ("¿En qué ciudad está la torre Eiffel?", "en París", ["parís", "paris", "en parís"], ["en londres", "en roma", "en madrid"]),
    ("¿Quién escribió Don Quijote de la Mancha?", "Miguel de Cervantes", ["cervantes", "miguel de cervantes"], ["borges", "neruda", "lope de vega"]),
    ("¿Quién pintó la Mona Lisa?", "Leonardo da Vinci", ["leonardo da vinci", "da vinci", "leonardo"], ["picasso", "van gogh", "dalí"]),
    ("¿Quién pintó el Guernica?", "Pablo Picasso", ["picasso", "pablo picasso"], ["dalí", "goya", "van gogh"]),
    ("¿Quién escribió Cien años de soledad?", "Gabriel García Márquez", ["gabriel garcía márquez", "garcía márquez", "gabo"], ["borges", "cortázar", "neruda"]),
    ("¿Cuántos días tiene un año bisiesto?", "366", ["366"], ["365", "360", "364"]),
    ("¿Cuántos minutos tiene una hora?", "60", ["60", "sesenta"], ["100", "30", "50"]),
    ("¿Cuántos jugadores tiene un equipo de fútbol en la cancha?", "once", ["once", "11"], ["diez", "nueve", "doce"]),
    ("¿Qué día viene después del jueves?", "el viernes", ["viernes", "el viernes"], ["el sábado", "el miércoles", "el lunes"]),
    ("¿Cuántos lados tiene un hexágono?", "seis", ["seis", "6"], ["cinco", "ocho", "siete"]),
    ("¿Cuánto es 7 por 8?", "56", ["56", "cincuenta y seis"], ["54", "48", "64"]),
    ("¿Cuánto es 9 por 6?", "54", ["54", "cincuenta y cuatro"], ["56", "45", "63"]),
    ("¿Cuánto es 12 más 15?", "27", ["27", "veintisiete"], ["26", "28", "17"]),
    ("¿Cuánto es la mitad de 50?", "25", ["25", "veinticinco"], ["20", "30", "15"]),
]

# ====================================================================== registro de generadores dinámicos
GENERATORS = [
    ("capital", 22, gen_capital),
    ("math", 26, gen_math),
    ("math_extra", 6, gen_math_extra),
    ("calendar", 8, gen_calendar),
    ("translate", 9, gen_translate),
]
