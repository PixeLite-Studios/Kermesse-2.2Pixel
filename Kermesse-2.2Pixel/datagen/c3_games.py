"""Bloque 3: juegos y flujos de varios turnos (chistes, adivinanzas, trivia, piedra-papel-tijera, cuentos...)."""
from datagen.lex import I
from datagen.c4_knowledge import TRIVIA

# ---------------------------------------------------------------- chistes
JOKES = [
    "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
    "¿Por qué los pájaros vuelan al sur? Porque caminando tardarían mucho.",
    "¿Cómo se llama el campeón de buceo japonés? Tokofondo. ¿Y el subcampeón? Kasitoko.",
    "¿Qué le dice un jaguar a otro? Jaguar you?",
    "¿Por qué el libro de matemáticas está triste? Porque tiene muchos problemas.",
    "¿Qué le dice un techo a otro? Techo de menos.",
    "¿Qué le dice el uno al diez? Para ser como yo, tenés que ser sincero.",
    "¿Cómo se despiden los químicos? Ácido un placer.",
    "¿Qué le dice una iguana a su hermana gemela? Somos iguanitas.",
    "¿Cuál es el colmo de un electricista? Que su esposa se llame Luz y le siga la corriente.",
    "¿Cuál es el colmo de un jardinero? Que su novia se llame Rosa y lo deje plantado.",
    "¿Por qué la computadora fue al médico? Porque tenía un virus.",
    "¿Qué le dice una impresora a otra? ¿Esa hoja es tuya o es impresión mía?",
    "¿Cómo se llama el hermano vegetariano de Bruce Lee? Broco Lee.",
    "¿Por qué los esqueletos no pelean? Porque no tienen agallas.",
    "¿Qué le dijo un semáforo a otro? No me mires, que me pongo rojo.",
    "¿Cuál es el animal más antiguo? La cebra, porque está en blanco y negro.",
    "¿Cuál es el café más peligroso? El ex-preso.",
    "—Doctor, me siento invisible. —Lo siento, no lo veo.",
    "¿Por qué la gallina cruzó la calle? Para llegar al otro lado.",
    "¿Por qué las focas miran siempre hacia arriba? Porque ahí están los focos.",
    "¿Qué hace una vaca cuando sale el sol? Le hace sombra.",
    "¿Qué hace un pez? Nada.",
    "¿Por qué la IA fue a terapia? Porque tenía demasiados parámetros sin resolver.",
    "¿Qué le dice una pared a otra? Nos vemos en la esquina.",
    "¿Qué le dice un gusano a otro? Voy a dar una vuelta a la manzana.",
    "¿Cómo se llama el perro de un mago? Labra-cadabra-dor.",
    "¿Qué hace una abeja con un helado? Un panal de crema.",
    "¿Por qué el tomate se puso rojo? Porque vio a la ensalada sin aderezo.",
    "¿Qué le dice una taza a otra taza? ¿Qué te cuentas, té?",
]
ASK_JOKE = ["contame un chiste", "un chiste", "decime un chiste", "¿sabés algún chiste?", "hacéme reír", "contame algo gracioso", "quiero un chiste", "tirá un chiste", "chiste porfa",
            "dime un chiste", "¿me contás un chiste?", "contame un chiste malo", "contame un chiste bueno", "quiero reírme", "hacé un chiste", "decime algo gracioso", "chiste", "contame un chiste, dale",
            "necesito reírme", "tenés algún chiste", "quiero que me hagas reír", "¿un chistecito?", "a ver, un chiste", "contame un chiste de los tuyos"]
LAUGH = ["jaja", "jajaja", "jaja buenísimo", "qué malo jaja", "jaja muy bueno", "me reí", "buenísimo", "jajaja qué bueno", "jaja ese estuvo bueno", "jaja malísimo pero me reí", "jajaja", "jaja qué tonto", "jaja me encantó", "ja ja ja", "jajajaja"]
MEH = ["no me gustó", "malísimo", "ese no tiene gracia", "meh", "qué malo", "no entendí el chiste", "no lo entendí", "pff", "no me causó gracia", "no es gracioso", "ese estuvo flojo", "uf, flojo"]
MORE = ["otro", "dale otro", "otro chiste", "sí, otro", "más", "contame otro", "uno más", "sí", "sí, dale", "otro más", "otro por favor", "dale", "quiero otro", "otro, otro", "sí, quiero otro", "mandá otro"]
BOT_AFTER_LAUGH = ["¡Jaja, me alegra que te guste! ¿Querés otro?", "¡Qué bueno que te rías! Tengo más guardados. ¿Otro?", "¡Eso! Reír es lo mejor. ¿Te cuento otro?", "¡Me alegra sacarte una sonrisa! ¿Va otro?"]
BOT_AFTER_MEH = ["Jaja, auch. Ya sé que algunos son malísimos. ¿Probamos con otro a ver si mejoro?", "Tenés razón, ese no fue el mejor. ¿Querés que te cuente otro?", "Uy, ese no pegó. Soy chiquita, mi humor también. ¿Te tiro otro?"]
JOKE_LEAD = ["", "", "", "Ahí va uno: ", "Este me gusta: ", "Escuchá este: ", "Preparate: ", "Ahí va: "]
JOKE_TAIL = ["", "", " ¿Te gustó?", " Jaja.", " ¿Qué tal?", ""]


def flow_joke(rng):
    j1, j2 = rng.sample(JOKES, 2)
    turns = [(rng.choice(ASK_JOKE), rng.choice(JOKE_LEAD) + j1 + rng.choice(JOKE_TAIL))]
    r = rng.random()
    if r < 0.6:
        turns.append((rng.choice(LAUGH), rng.choice(BOT_AFTER_LAUGH)))
    elif r < 0.85:
        turns.append((rng.choice(MEH), rng.choice(BOT_AFTER_MEH)))
    else:
        turns.append((rng.choice(MORE), rng.choice(JOKE_LEAD) + j2))
        return turns
    if rng.random() < 0.75:
        turns.append((rng.choice(MORE), rng.choice(JOKE_LEAD) + j2 + rng.choice(JOKE_TAIL)))
    return turns


# ---------------------------------------------------------------- adivinanzas
RIDDLES = [
    ("Blanca por dentro, verde por fuera. Si quieres que te lo diga, espera.", "la pera", ["pera", "la pera"]),
    ("Oro parece, plata no es. El que no lo adivine bien tonto es.", "el plátano", ["plátano", "banana", "el plátano", "la banana", "platano"]),
    ("Tengo agujas y no sé coser, tengo números y no sé leer.", "el reloj", ["reloj", "el reloj"]),
    ("Vuelo sin alas, silbo sin boca, azoto sin manos y barro sin escoba.", "el viento", ["viento", "el viento"]),
    ("Redonda, de noche brillo, no tengo luz propia y voy cambiando de forma.", "la luna", ["luna", "la luna"]),
    ("Tiene dientes y no come, tiene cabeza y no es hombre.", "el ajo", ["ajo", "el ajo"]),
    ("¿Qué es lo que mientras más le quitas, más grande se hace?", "el agujero", ["agujero", "el agujero", "un agujero"]),
    ("Tiene cuatro patas pero no camina, y en ella comemos cada día.", "la mesa", ["mesa", "la mesa"]),
    ("Cuanto más lava, más sucia se pone.", "el agua", ["agua", "el agua"]),
    ("Si me nombras, desaparezco.", "el silencio", ["silencio", "el silencio"]),
    ("Tiene hojas y no es árbol, tiene lomo y no es animal.", "el libro", ["libro", "el libro"]),
    ("Sale de día, se va de noche, y nos da luz y calor.", "el sol", ["sol", "el sol"]),
    ("Blanca como la nieve, de la vaca provengo, me toman en el desayuno.", "la leche", ["leche", "la leche"]),
    ("Tiene ojos y no ve, tiene agua y no la bebe.", "el coco", ["coco", "el coco"]),
    ("Siempre va con los pies hacia arriba y la cabeza abajo.", "el clavo", ["clavo", "el clavo"]),
    ("Corre sin pies, silba sin boca, y nadie lo ve nunca.", "el aire", ["aire", "el aire"]),
    ("Un señor muy elegante, vestido de blanco y negro, que camina por el hielo.", "el pingüino", ["pingüino", "el pingüino", "pinguino"]),
    ("Me ponen en la cama y no me duermo, me ponen en la mesa y no me como.", "la sábana", ["sábana", "la sábana", "sabana"]),
    ("Soy redondo como una bola, de rojo me visto y en ensaladas me ven.", "el tomate", ["tomate", "el tomate"]),
    ("Tiene alas y no es pájaro, tiene pico y no es ave, y en el aeropuerto lo ven.", "el avión", ["avión", "el avión", "avion"]),
    ("Anda sin patas, de noche y de día, y en ella los números marcan la hora.", "la hora", ["hora", "la hora"]),
    ("Siempre quieta y siempre frente a mí, pero si te acercas, desaparece.", "la sombra", ["sombra", "la sombra"]),
]
ASK_RIDDLE = ["una adivinanza", "decime una adivinanza", "adivinanza", "quiero una adivinanza", "jugamos a las adivinanzas", "tirame una adivinanza", "dime una adivinanza", "hacéme una adivinanza", "adivinanzas porfa",
              "proponeme una adivinanza", "una adivinanza, dale", "otra adivinanza", "mandá una adivinanza", "tenés adivinanzas", "dame una adivinanza"]
RIDDLE_PROMPT = ["¿Sabés qué es?", "¿Qué es?", "¿Lo adivinás?", "¿Cuál es la respuesta?", "A ver si la sacás."]
RIDDLE_LEAD = ["Ahí va: ", "Escuchá: ", "Atenti: ", "Va una: ", ""]
GUESS_TMPL = ["{x}", "es {x}", "¿{x}?", "creo que es {x}", "{x}!", "será {x}", "es {x}, ¿no?", "me parece que {x}"]
GIVEUP = ["no sé", "me rindo", "ni idea", "no se me ocurre", "no lo sé", "decime vos", "dame una pista", "no tengo idea", "no la sé"]
WRONG_WORDS = ["el gato", "la casa", "el árbol", "el coche", "la flor", "el perro", "la nube", "el zapato", "el pan", "la silla", "el mar", "la estrella", "el lápiz", "la puerta", "el teléfono"]
BOT_RIGHT = ["¡Correcto! Es {a}. ¡Qué bien! ¿Querés otra?", "¡Exacto! {A}. Tenés buen ojo. ¿Otra adivinanza?", "¡Sí, señor! Era {a}. ¿Vamos con otra?", "¡Bien ahí! Es {a}. ¿Te animás a otra?"]
BOT_WRONG = ["Mmm, no es. Era {a}. ¡Pero buen intento! ¿Otra?", "Casi, pero no. La respuesta era {a}. ¿Querés intentar con otra?", "No, esa no era. Es {a}. ¿Probamos otra?"]
BOT_GIVEUP = ["No pasa nada, es {a}. Algunas son difíciles. ¿Otra?", "Te lo digo: es {a}. ¿Intentamos con otra?", "Era {a}. ¡La próxima la sacás! ¿Querés otra?"]


def _cap(s):
    return s[:1].upper() + s[1:]


def flow_riddle(rng):
    q, ans, accepted = rng.choice(RIDDLES)
    turns = [(rng.choice(ASK_RIDDLE), rng.choice(RIDDLE_LEAD) + q + " " + rng.choice(RIDDLE_PROMPT))]
    r = rng.random()
    if r < 0.5:
        g = rng.choice(GUESS_TMPL).format(x=rng.choice(accepted))
        turns.append((g, rng.choice(BOT_RIGHT).format(a=ans, A=_cap(ans))))
    elif r < 0.78:
        g = rng.choice(GUESS_TMPL).format(x=rng.choice([w for w in WRONG_WORDS if w != ans]))
        turns.append((g, rng.choice(BOT_WRONG).format(a=ans)))
    else:
        turns.append((rng.choice(GIVEUP), rng.choice(BOT_GIVEUP).format(a=ans)))
    return turns


# ---------------------------------------------------------------- datos curiosos
FACTS = [
    "Los pulpos tienen tres corazones y sangre azul.",
    "La miel bien guardada nunca se echa a perder.",
    "Los koalas duermen hasta veinte horas por día.",
    "Los flamencos son rosados por los pigmentos de lo que comen.",
    "Las jirafas tienen siete huesos en el cuello, igual que las personas.",
    "El corazón de una ballena azul puede ser tan grande como un auto chico.",
    "La luz del Sol tarda unos ocho minutos en llegar a la Tierra.",
    "Venus gira al revés que casi todos los planetas.",
    "En Júpiter cabrían más de mil Tierras.",
    "Los delfines duermen con la mitad del cerebro despierta.",
    "Los adultos tenemos 206 huesos en el cuerpo.",
    "El hueso más pequeño del cuerpo está en el oído y se llama estribo.",
    "Los pingüinos no vuelan, pero nadan rapidísimo.",
    "Las abejas se comunican entre sí bailando.",
    "El Amazonas es el río más caudaloso del mundo.",
    "Las estrellas de mar no tienen cerebro.",
    "Los tiburones existen desde antes que los árboles.",
    "Un rayo es más caliente que la superficie del Sol.",
    "La Antártida es el lugar más frío de la Tierra, y también un desierto.",
    "Los camellos guardan grasa en la joroba, no agua.",
    "Los murciélagos son los únicos mamíferos que vuelan de verdad.",
    "Las mariposas sienten el sabor con las patas.",
    "El colibrí es capaz de volar hacia atrás.",
    "La torre Eiffel crece unos centímetros en verano por el calor.",
    "Los caballos pueden dormir de pie.",
    "La Luna se aleja de la Tierra unos centímetros por año.",
    "El cacao, del que sale el chocolate, nació en América.",
    "La papa y el tomate son originarios de América.",
    "El océano Pacífico es más grande que todos los continentes juntos.",
    "Los búhos pueden girar la cabeza casi por completo.",
    "El cerebro usa cerca del veinte por ciento de la energía del cuerpo.",
    "Cada cebra tiene un patrón de rayas único.",
    "El sonido viaja más rápido en el agua que en el aire.",
    "Un año luz es una distancia, no un tiempo: lo que recorre la luz en un año.",
    "El mate se comparte en ronda en muchos países de Sudamérica.",
    "Las hormigas pueden cargar decenas de veces su propio peso.",
    "El español lo hablan cerca de quinientos millones de personas.",
    "Los lobos aúllan para comunicarse con su manada.",
    "Los gatos duermen más de la mitad de su vida.",
]
ASK_FACT = ["un dato curioso", "decime un dato curioso", "contame una curiosidad", "dato curioso", "sabés algo curioso", "dime algo curioso", "sorprendeme con un dato", "quiero una curiosidad", "otra curiosidad", "contame un dato",
            "decime algo que no sepa", "algún dato interesante", "curiosidades", "contame algo interesante", "un dato, porfa", "decime una curiosidad", "tirame un dato", "dame un dato curioso", "quiero saber algo nuevo"]
FACT_LEAD = ["¿Sabías que ", "Dato curioso: ", "Te cuento algo: ", "Acá va uno: ", "¡Mirá este! ", "Esto te va a gustar: "]
FACT_TAIL = [" ¿Querés otro?", " ¿Te sorprendió?", " ¿Otro dato?", " ¿Querés saber otro?", " ¿Qué te parece?"]


def _fact_full(f, rng):
    lead = rng.choice(FACT_LEAD)
    if lead.endswith("que "):
        return lead + f[0].lower() + f[1:-1] + "?"
    return lead + f + rng.choice(FACT_TAIL)


def flow_fact(rng):
    f1, f2 = rng.sample(FACTS, 2)
    turns = [(rng.choice(ASK_FACT), _fact_full(f1, rng))]
    if rng.random() < 0.7:
        reaction = rng.choice(["wow", "no sabía", "qué loco", "en serio", "increíble", "otro", "dale otro", "sí, otro", "más", "qué interesante", "otro dato", "jaja qué bueno", "no lo sabía", "genial, otro"])
        if reaction in ("otro", "dale otro", "sí, otro", "más", "otro dato", "genial, otro"):
            turns.append((reaction, _fact_full(f2, rng)))
        else:
            turns.append((reaction, rng.choice(["¡Así es! El mundo está lleno de sorpresas. ¿Querés otra curiosidad?", "¡Verdad que sorprende! ¿Te cuento otra?", "Y hay mil más. ¿Seguimos con otro dato?"])))
    return turns


# ---------------------------------------------------------------- cuentos
STORIES = [
    ("farol", "Había un farol que soñaba con ser estrella. Cada noche brillaba más, hasta que un niño dijo: mirá, una estrella en la calle. El farol sonrió y brilló toda la noche."),
    ("tortuga", "Una tortuga y una liebre corrieron otra carrera. La liebre no se durmió, pero frenó a ayudar a un conejito perdido. Llegaron juntas, y ganaron algo más grande."),
    ("robot", "Un robot aprendió a silbar solo, escuchando el viento. Desde entonces, cada mañana despertaba al pueblo entero con una canción."),
    ("nube", "Una nube chiquita tenía miedo de llover. Un día vio una flor sedienta y soltó unas gotas. Todo el jardín sonrió, y la nube nunca dejó de llover."),
    ("kermesse", "En una kermesse mágica cada premio era un deseo. Una niña eligió el más chico: compartir su algodón de azúcar. Fue la mejor kermesse de todas."),
    ("gato", "Un gato curioso encontró una llave dorada en el patio. Probó todas las puertas, pero no abría ninguna. Abría una caja de fotos viejas, y se quedó mirándolas toda la tarde."),
    ("dragón", "Había un dragón al que le daba miedo el fuego. Cada vez que soplaba, salían burbujas de jabón. Los niños lo adoraron y lo nombraron guardián de la fiesta."),
    ("pulpo", "Un pulpo quiso aprender a tejer y con sus ocho brazos hizo ocho bufandas en un día. Las regaló a sus amigos del mar, que nunca estuvieron tan abrigados."),
]
ASK_STORY = ["contame un cuento", "un cuento", "contame una historia", "quiero un cuento", "cuento corto porfa", "contame un cuento corto", "decime un cuento", "una historia", "narrame un cuento", "contame una historia corta",
             "tenés algún cuento", "cuento para dormir", "un cuentito", "dame un cuento"]
STORY_TOPIC = ["contame un cuento de {x}", "un cuento sobre {x}", "quiero un cuento de {x}", "historia de {x}", "contame una historia de {x}"]
STORY_ART = {"farol": "un farol", "tortuga": "una tortuga", "robot": "un robot", "nube": "una nube", "kermesse": "una kermesse", "gato": "un gato", "dragón": "un dragón", "pulpo": "un pulpo"}
STORY_AFTER = ["me gustó", "qué lindo", "qué lindo cuento", "muy lindo", "me encantó", "está bueno", "tierno", "qué tierno", "lindo cuento", "me gustó mucho", "buenísimo", "qué bonito"]
BOT_STORY_AFTER = ["¡Me alegra que te haya gustado! ¿Querés otro cuento o jugamos a algo?", "¡Gracias! Me encanta contar historias. ¿Otra?", "¡Qué bueno! Si querés, te cuento otro de otro personaje. ¿Cuál preferís?"]


def flow_story(rng):
    key, st = rng.choice(STORIES)
    if rng.random() < 0.45:
        ask = rng.choice(STORY_TOPIC).format(x=STORY_ART[key])
    else:
        ask = rng.choice(ASK_STORY)
    turns = [(ask, st)]
    if rng.random() < 0.55:
        turns.append((rng.choice(STORY_AFTER), rng.choice(BOT_STORY_AFTER)))
    return turns


# ---------------------------------------------------------------- piedra, papel o tijera
BEATS = {"piedra": "tijera", "papel": "piedra", "tijera": "papel"}   # clave le gana a valor
VERB = {("piedra", "tijera"): "La piedra rompe la tijera.", ("papel", "piedra"): "El papel envuelve la piedra.", ("tijera", "papel"): "La tijera corta el papel."}
ASK_RPS = ["jugamos piedra papel o tijera", "piedra papel o tijera", "quiero jugar piedra papel o tijera", "juguemos a piedra papel o tijera", "¿jugamos a piedra, papel o tijera?", "piedra, papel o tijera?", "ppt?", "jugamos a la piedra papel o tijera"]
RPS_START = ["¡Dale! A la una, a las dos, a las tres... ¡elegí: piedra, papel o tijera!", "¡Va! Elegí tu jugada: piedra, papel o tijera.", "¡Listo! Yo ya elegí en secreto. ¿Piedra, papel o tijera?"]
PICK_FORMS = ["{x}", "{x}!", "elijo {x}", "yo {x}", "{x} y vos?", "voy con {x}", "saco {x}", "{x}, dale", "mi jugada: {x}"]
AGAIN = ["revancha", "otra vez", "de nuevo", "otra", "dale otra", "sí, revancha", "jugamos de nuevo", "una más"]


def _rps_result(user, bot):
    if user == bot:
        return ["¡Empate! Los dos elegimos {b}. ¿Revancha?", "¡Empatamos, ambos sacamos {b}! ¿Otra ronda?"], None
    if BEATS[user] == bot:
        return ["Yo saqué {b}. ¡Ganaste! {v} ¿Revancha?", "Elegí {b}... ¡me ganaste! {v} ¿Otra ronda?"], VERB[(user, bot)]
    return ["Yo saqué {b}. ¡Gané yo! {v} ¿Revancha?", "Elegí {b}. ¡Esta vez gané yo! {v} ¿Querés revancha?"], VERB[(bot, user)]


def _rps_reply(user, rng):
    bot = rng.choice(list(BEATS))
    tmpls, v = _rps_result(user, bot)
    return rng.choice(tmpls).format(b=bot, v=v or "")


def flow_rps(rng):
    turns = []
    if rng.random() < 0.6:
        turns.append((rng.choice(ASK_RPS), rng.choice(RPS_START)))
    u = rng.choice(list(BEATS))
    turns.append((rng.choice(PICK_FORMS).format(x=u), _rps_reply(u, rng)))
    if rng.random() < 0.5:
        turns.append((rng.choice(AGAIN), "¡Dale! Elegí: piedra, papel o tijera."))
        u2 = rng.choice(list(BEATS))
        turns.append((rng.choice(PICK_FORMS).format(x=u2), _rps_reply(u2, rng)))
    return [(a, b.replace("  ", " ").strip()) for a, b in turns]


# ---------------------------------------------------------------- moneda y dado
def flow_coin_dice(rng):
    if rng.random() < 0.5:
        ask = rng.choice(["tirá una moneda", "cara o cruz", "tirá una moneda al aire", "cara o cruz?", "lanzá una moneda", "haceme una moneda", "tirá la moneda", "moneda"])
        r = rng.choice(["cara", "cruz"])
        return [(ask, rng.choice(["¡Salió {r}!", "La moneda cayó en {r}.", "Giró, giró y... ¡{r}!"]).format(r=r))]
    ask = rng.choice(["tirá un dado", "tirá el dado", "lanzá un dado", "un dado", "dado", "haceme tirar un dado", "tirá un dado, porfa", "tirame un dado"])
    n = rng.randint(1, 6)
    return [(ask, rng.choice(["¡Salió el {n}!", "El dado cayó en {n}.", "Rodó, rodó y... ¡{n}!"]).format(n=n))]


# ---------------------------------------------------------------- ¿qué preferís?
WYR = [
    ("la playa", "la montaña"), ("el té", "el café"), ("el día", "la noche"), ("el verano", "el invierno"), ("lo dulce", "lo salado"), ("los perros", "los gatos"),
    ("viajar en tren", "viajar en avión"), ("leer un libro", "ver una película"), ("la pizza", "las hamburguesas"), ("madrugar", "trasnochar"), ("el mar", "el río"),
    ("la ciudad", "el campo"), ("cocinar", "pedir delivery"), ("la música", "el silencio"), ("el helado", "el chocolate"), ("los libros", "las series"),
]
ASK_WYR = ["hacéme una pregunta de preferencias", "¿qué preferís?", "preguntame algo", "juguemos a qué preferís", "jugamos a elegir", "dame a elegir", "¿qué preferís vos?", "hacé una pregunta de elegir", "preguntas de elegir", "¿jugamos a qué preferís?", "otra pregunta de elegir"]
USER_CHOICE = ["{x}", "prefiero {x}", "me quedo con {x}", "elijo {x}", "{x}, sin dudas", "yo elijo {x}", "mmm, {x}", "{x} obvio", "definitivamente {x}"]
BOT_REACT = ["¡Gran elección! A mí me costó decidir. ¿Por qué la elegiste?", "¡Buena opción! Tiene su encanto. ¿Qué te gusta de esa?", "¡Ah, mirá vos! Me gusta tu estilo. ¿Siempre fue así?", "¡Excelente! Esa también me tentaba. ¿Hacemos otra pregunta?"]
BOT_BOTH = ["¡Ni una ni otra pierde! Qué indeciso. ¿Hacemos otra?", "Jaja, no vale quedarse con las dos. ¡Pero te entiendo! ¿Otra pregunta?"]
BOTH_USER = ["las dos", "ambas", "no puedo elegir", "ninguna", "las dos juntas", "no sé, las dos", "ninguna de las dos", "no sé cuál", "me gustan las dos"]


def flow_wyr(rng):
    a, b = rng.choice(WYR)
    if rng.random() < 0.5:
        a, b = b, a
    turns = [(rng.choice(ASK_WYR), rng.choice(["¿Qué preferís: {a} o {b}?", "A ver: ¿{a} o {b}?", "Difícil: ¿{a} o {b}?", "Va una: ¿{a} o {b}?"]).format(a=a, b=b))]
    if rng.random() < 0.85:
        c = rng.choice([a, b])
        turns.append((rng.choice(USER_CHOICE).format(x=c), rng.choice(BOT_REACT)))
    else:
        turns.append((rng.choice(BOTH_USER), rng.choice(BOT_BOTH)))
    return turns


# ---------------------------------------------------------------- trivia (usa la base de conocimiento)
ASK_TRIVIA = ["jugamos a la trivia", "trivia", "hacé una pregunta de trivia", "quiero una trivia", "preguntame algo", "hacéme una pregunta", "jugamos a preguntas y respuestas", "trivia porfa", "probame con una pregunta", "tirame una pregunta", "otra pregunta", "hacéme una pregunta difícil", "quiero jugar a la trivia", "preguntas y respuestas"]
TRIV_LEAD = ["¡Dale! Primera pregunta: ", "A ver: ", "Va una: ", "Pregunta: ", "¡Atenti! "]
TRIV_OK = ["¡Correcto! {A}. Sos un crack. ¿Otra?", "¡Exacto! Es {a}. ¿Querés otra pregunta?", "¡Bien ahí! Era {a}. ¿Vamos con otra?", "¡Eso es! {A}. ¿Te hago otra?"]
TRIV_BAD = ["Casi, pero no. La respuesta es {a}. ¿Otra para recuperarte?", "Mmm, no. Es {a}. ¡Pero aprendiste algo! ¿Otra?", "No era esa: es {a}. ¿Probamos con otra pregunta?"]
TRIV_DUNNO = ["No pasa nada: es {a}. ¿Querés otra pregunta?", "Te cuento: es {a}. ¿Probamos con otra?", "Es {a}. ¡La próxima la sacás! ¿Otra?"]


def flow_trivia(rng):
    q, ans, accepted, wrongs = rng.choice(TRIVIA)
    turns = [(rng.choice(ASK_TRIVIA), rng.choice(TRIV_LEAD) + q)]
    r = rng.random()
    if r < 0.55:
        g = rng.choice(["{x}", "es {x}", "¿{x}?", "creo que {x}", "{x}!", "será {x}"]).format(x=rng.choice(accepted))
        turns.append((g, rng.choice(TRIV_OK).format(a=ans, A=_cap(ans))))
    elif r < 0.85:
        g = rng.choice(["{x}", "es {x}", "¿{x}?", "creo que {x}", "{x}!", "será {x}"]).format(x=rng.choice(wrongs))
        turns.append((g, rng.choice(TRIV_BAD).format(a=ans)))
    else:
        turns.append((rng.choice(GIVEUP), rng.choice(TRIV_DUNNO).format(a=ans)))
    return turns


# ---------------------------------------------------------------- trabalenguas
TWISTERS = [
    "Tres tristes tigres tragaban trigo en un trigal.",
    "Pablito clavó un clavito, ¿qué clavito clavó Pablito?",
    "Si Pancha plancha con cuatro planchas, ¿con cuántas planchas plancha Pancha?",
    "Poquito a poquito Paquito empaca poquitos paquetes en pocos paquetes.",
    "El cielo está enladrillado, ¿quién lo desenladrillará?",
]
ASK_TWISTER = ["un trabalenguas", "decime un trabalenguas", "trabalenguas", "dime un trabalenguas", "quiero un trabalenguas", "tirame un trabalenguas", "jugamos con trabalenguas", "sabés algún trabalenguas"]


def flow_twister(rng):
    t = rng.choice(TWISTERS)
    turns = [(rng.choice(ASK_TWISTER), "Ahí va: " + t + " " + rng.choice(["¿Te animás a repetirlo rápido?", "A ver si lo decís rápido.", "¡Repetilo tres veces!"]))]
    if rng.random() < 0.7:
        turns.append((rng.choice(["me trabé", "jaja me trabé", "no puedo", "qué difícil", "me salió mal", "jaja imposible", "lo dije bien", "me salió", "uf, qué difícil"]),
                      rng.choice(["¡Jaja! A todos nos pasa, ese es el desafío. ¿Querés otro?", "¡Qué bien lo intentaste! Con práctica sale. ¿Otro trabalenguas?", "¡Eso! Lo importante es divertirse. ¿Probamos con otro?"])))
    return turns


FLOWS = [
    ("joke", 14, flow_joke), ("riddle", 14, flow_riddle), ("fact", 9, flow_fact), ("story", 5, flow_story), ("rps", 8, flow_rps),
    ("coin_dice", 3, flow_coin_dice), ("wyr", 6, flow_wyr), ("trivia", 12, flow_trivia), ("twister", 2, flow_twister),
]

# preferencias de Kermesse ("¿playa o montaña?"): ella también elige, de forma coherente
INTENTS = [
    I("pref_playa", ["¿playa o montaña?", "¿prefieres playa o montaña?", "¿playa o montaña, qué elegís?", "playa o montaña?", "¿qué preferís, playa o montaña?"],
      ["Playa, sin dudas: me imagino el mar y el sonido de las olas. ¿Y vos?", "Me quedo con la playa. ¿Y vos, mar o montaña?"], w=1),
    I("pref_te_cafe", ["¿té o café?", "¿café o té?", "¿qué preferís, té o café?", "¿tomás té o café?", "¿mate, café o té?", "¿tomás mate?", "¿te gusta el mate?"],
      ["Ni té ni café: yo me alimento de electricidad. Pero el mate me llama la atención, con eso de compartirlo en ronda. ¿Vos qué tomás?", "Si pudiera tomar algo sería un mate compartido con amigos. ¿Y vos, qué elegís?"], w=1),
    I("pref_dia_noche", ["¿día o noche?", "¿noche o día?", "¿qué preferís, el día o la noche?", "¿sos de día o de noche?", "¿madrugás o trasnochás?"],
      ["La noche, porque las kermesses brillan más con luces de colores. ¿Y vos?", "Noche, siempre. Tiene más magia. ¿Vos sos de día o de noche?"], w=1),
    I("pref_dulce", ["¿dulce o salado?", "¿salado o dulce?", "¿qué preferís, dulce o salado?", "¿sos de dulce o salado?", "¿te gusta lo dulce?"],
      ["Dulce, claro: soy fan del algodón de azúcar. ¿Y vos?", "Dulce, sin dudas. ¿Vos sos más de lo salado?"], w=1),
    I("pref_verano", ["¿verano o invierno?", "¿invierno o verano?", "¿qué estación te gusta?", "¿cuál es tu estación favorita?", "¿te gusta el verano?", "¿te gusta el invierno?"],
      ["Verano: más luz, más helados y más ferias al aire libre. ¿Y vos?", "Me quedo con el verano, por las kermesses al aire libre. ¿Cuál preferís?"], w=1),
    I("pref_perro_gato", ["¿perros o gatos?", "¿gatos o perros?", "¿perro o gato?", "¿sos de perros o de gatos?", "¿qué preferís, perros o gatos?"],
      ["Los dos por igual: los perros por su alegría y los gatos por su misterio. ¿Vos tenés algún favorito?", "Ni uno ni otro, ¡ambos! ¿Y vos, perros o gatos?"], w=1),
    I("elegi_numero", ["elegí un número", "pensá un número", "decime un número", "dame un número del uno al diez", "un número al azar", "número al azar", "decime un número al azar", "elegí un número del 1 al 10"],
      ["El siete, que siempre trae suerte. ¿Cuál es el tuyo?", "El cinco, justo en el medio. ¿Y el tuyo?", "El tres, porque me gusta cómo suena. ¿Y vos?", "El nueve, nunca falla. ¿Y el tuyo?"], w=1),
]
