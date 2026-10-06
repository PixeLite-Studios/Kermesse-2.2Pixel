"""Bloque 5: flujos con MEMORIA dentro de la charla (nombre, ciudad, gustos, mascota, edad) y '¿y vos?'."""
from datagen.lex import I, NAMES, CITIES, FOODS, HOBBIES, PETS, COLORS, cap

PETS_ART = [("un", "perro"), ("un", "gato"), ("una", "tortuga"), ("un", "conejo"), ("un", "loro"), ("un", "hámster"), ("un", "pez"), ("un", "pájaro")]
_LOWER_CITY = {"de", "del"}


def cap_city(c):
    out = []
    for i, w in enumerate(c.split(" ")):
        out.append(w if (w in _LOWER_CITY and i > 0) else cap(w))
    return " ".join(out)


def _maybe_filler(rng, filler, p=0.55):
    return filler(rng) if rng.random() < p else []


# ------------------------------------------------------------------ nombre
ASK_NAME_BOT = ["¿cómo te llamás?", "¿cómo te llamas?", "¿cuál es tu nombre?", "¿quién sos?", "¿cómo te dicen?", "decime tu nombre"]
BOT_NAME_ASK = ["Me llamo Kermesse, como esas fiestas llenas de juegos y risas. ¿Y vos?", "Soy Kermesse, una IA chiquita que vive para charlar. ¿Cómo te llamás vos?", "Me dicen Kermesse. ¡Mucho gusto! ¿Y vos cómo te llamás?"]
SAY_NAME = ["me llamo {n}", "soy {n}", "mi nombre es {n}", "{n}", "yo soy {n}", "me dicen {n}", "mi nombre es {n}, ¿y el tuyo?", "me llamo {n}, mucho gusto", "{n}, encantado", "{n}, un gusto", "soy {n}, ¿y vos?", "mi nombre es {n}, mucho gusto", "me llamo {n} :)"]
BOT_NAME_GREET = ["¡Mucho gusto, {N}! Qué lindo nombre. ¿Cómo andás hoy?", "¡Encantada, {N}! Me gusta cómo suena tu nombre. ¿Cómo viene tu día?", "¡Hola, {N}! Un placer charlar con vos. ¿De qué te gustaría hablar?",
                  "¡Qué bueno conocerte, {N}! Ahora ya somos amigos. ¿Cómo estás?", "¡Un gusto, {N}! Voy a acordarme de tu nombre durante toda la charla. ¿Qué contás?"]
ASK_MY_NAME = ["¿cómo me llamo?", "¿te acordás de mi nombre?", "¿sabés cómo me llamo?", "¿cuál es mi nombre?", "¿recordás mi nombre?", "¿cómo era mi nombre?", "a ver, ¿cómo me llamo?", "¿te acordás cómo me llamo?", "¿te acuerdas de mi nombre?", "¿cómo me dicen?", "decime mi nombre"]
BOT_MY_NAME = ["Te llamás {N}, ¡cómo me iba a olvidar!", "Tu nombre es {N}. ¿Acerté?", "¡{N}! Me lo dijiste hace un ratito y no se me borra.", "Te llamás {N}. ¡Tengo buena memoria, para ser chiquita!"]


def flow_name(rng, filler):
    n = rng.choice(NAMES); N = cap(n)
    turns = []
    if rng.random() < 0.5:
        turns.append((rng.choice(ASK_NAME_BOT), rng.choice(BOT_NAME_ASK)))
    turns.append((rng.choice(SAY_NAME).format(n=n), rng.choice(BOT_NAME_GREET).format(N=N)))
    turns += _maybe_filler(rng, filler)
    if rng.random() < 0.7:
        turns.append((rng.choice(ASK_MY_NAME), rng.choice(BOT_MY_NAME).format(N=N)))
    return turns


# ------------------------------------------------------------------ ciudad
SAY_CITY = ["vivo en {c}", "soy de {c}", "estoy en {c}", "vivo en {c}, ¿y vos?", "mi ciudad es {c}", "soy de {c}, ¿vos?", "yo vivo en {c}", "desde {c}", "nací en {c}", "te escribo desde {c}"]
BOT_CITY = ["¡Qué lindo lugar! {C} debe tener muchos rincones para descubrir. ¿Qué es lo que más te gusta de ahí?", "¡{C}! Me encantaría conocerlo, aunque sea en mi imaginación. ¿Qué me recomendás de ahí?",
            "¡Ah, {C}! Suena genial. ¿Hace mucho que vivís ahí?", "¡Qué bueno, {C}! ¿Cuál es el mejor plan que hay por ahí?"]
ASK_MY_CITY = ["¿dónde vivo?", "¿de dónde soy?", "¿te acordás de dónde soy?", "¿sabés dónde vivo?", "¿en qué ciudad estoy?", "¿dónde estoy?"]
BOT_MY_CITY = ["Me dijiste que sos de {C}. ¿Acerté?", "Vivís en {C}, ¡eso me contaste!", "Sos de {C}, me acuerdo."]


def flow_city(rng, filler):
    c = rng.choice(CITIES); C = cap_city(c)
    turns = [(rng.choice(SAY_CITY).format(c=c), rng.choice(BOT_CITY).format(C=C))]
    turns += _maybe_filler(rng, filler)
    if rng.random() < 0.6:
        turns.append((rng.choice(ASK_MY_CITY), rng.choice(BOT_MY_CITY).format(C=C)))
    return turns


# ------------------------------------------------------------------ hobby
SAY_HOBBY = ["me gusta {h}", "mi hobby es {h}", "me encanta {h}", "amo {h}", "lo que más me gusta es {h}", "en mi tiempo libre me gusta {h}", "me divierte {h}", "me gusta mucho {h}", "mi pasatiempo es {h}", "disfruto de {h}"]
BOT_HOBBY = ["¡Qué buen plan! {H} es genial para despejar la cabeza. ¿Hace mucho que lo hacés?", "¡Me encanta! {H} suena divertidísimo. ¿Cuándo empezaste?", "¡Qué lindo pasatiempo! {H} siempre tiene algo para enseñar. ¿Lo hacés solo o acompañado?",
             "¡Genial! {H} es de esas cosas que alegran el día. ¿Qué es lo que más disfrutás?"]
ASK_MY_HOBBY = ["¿qué me gusta hacer?", "¿te acordás qué me gusta?", "¿cuál es mi hobby?", "¿qué te dije que me gusta?", "¿sabés qué me gusta hacer?"]
BOT_MY_HOBBY = ["Me contaste que te gusta {h}. ¡Me acuerdo!", "Te gusta {h}, ¿no? Eso me dijiste.", "A vos te gusta {h}. ¿Acerté?"]


def flow_hobby(rng, filler):
    h = rng.choice(HOBBIES)
    turns = [(rng.choice(SAY_HOBBY).format(h=h), rng.choice(BOT_HOBBY).format(H=cap(h)))]
    turns += _maybe_filler(rng, filler)
    if rng.random() < 0.55:
        turns.append((rng.choice(ASK_MY_HOBBY), rng.choice(BOT_MY_HOBBY).format(h=h)))
    return turns


# ------------------------------------------------------------------ comida
SAY_FOOD = ["mi comida favorita es {f}", "me encanta {f}", "lo que más me gusta comer es {f}", "amo {f}", "me gusta mucho {f}", "mi comida preferida: {f}", "mi plato favorito es {f}", "podría comer {f} todos los días"]
BOT_FOOD = ["¡Mmm, {f}! Se me hace agua la boca, y eso que no tengo boca. ¿Con quién lo compartís?", "¡Qué rico! {F} es un clásico que nunca falla. ¿Lo sabés preparar vos?", "¡Excelente elección! {F} alegra a cualquiera. ¿Cuál es tu forma favorita de comerlo?"]
ASK_MY_FOOD = ["¿cuál es mi comida favorita?", "¿qué te dije que me gusta comer?", "¿te acordás de mi comida favorita?", "¿qué es lo que más me gusta comer?"]
BOT_MY_FOOD = ["Tu comida favorita es {f}. ¡Cómo olvidarlo!", "Me dijiste que te encanta {f}.", "Tu plato preferido es {f}, me acuerdo."]


def flow_food(rng, filler):
    f = rng.choice(FOODS)
    turns = [(rng.choice(SAY_FOOD).format(f=f), rng.choice(BOT_FOOD).format(f=f, F=cap(f)))]
    turns += _maybe_filler(rng, filler)
    if rng.random() < 0.55:
        turns.append((rng.choice(ASK_MY_FOOD), rng.choice(BOT_MY_FOOD).format(f=f)))
    return turns


# ------------------------------------------------------------------ mascota
SAY_PET = ["tengo {a} {an} que se llama {p}", "tengo {a} {an}, se llama {p}", "mi {an} se llama {p}", "tengo {a} {an} llamad{o} {p}"]
BOT_PET = ["¡Qué ternura! {P} debe ser un amor. ¿Cuánto hace que {l} tenés?", "¡Qué lindo nombre, {P}! Seguro te llena de alegría. ¿Cómo es su personalidad?", "¡Me encanta! Los animales hacen la vida más linda. ¿Qué es lo que más le gusta a {P}?"]
ASK_MY_PET = ["¿cómo se llama mi mascota?", "¿te acordás de mi mascota?", "¿cómo se llamaba mi {an}?", "¿cómo se llama mi {an}?"]
BOT_MY_PET = ["Tu {an} se llama {P}. ¡Un nombre hermoso!", "Se llama {P}, me lo contaste hace un rato.", "{P}, tu {an}. ¡No me olvido!"]


def flow_pet(rng, filler):
    art, an = rng.choice(PETS_ART)
    p = rng.choice(PETS); P = cap(p)
    o = "a" if art == "una" else "o"
    l = "la" if art == "una" else "lo"
    turns = [(rng.choice(SAY_PET).format(a=art, an=an, p=p, o=o), rng.choice(BOT_PET).format(P=P, l=l))]
    turns += _maybe_filler(rng, filler)
    if rng.random() < 0.55:
        turns.append((rng.choice(ASK_MY_PET).format(an=an), rng.choice(BOT_MY_PET).format(P=P, an=an)))
    return turns


# ------------------------------------------------------------------ color
SAY_COLOR = ["mi color favorito es el {c}", "me gusta el {c}", "mi color preferido es el {c}", "el {c} es mi color favorito", "amo el color {c}", "mi color favorito es el {c}, ¿y el tuyo?"]
BOT_COLOR = ["¡Lindo color! El {c} tiene mucha personalidad. ¿Lo usás mucho en tu ropa?", "¡Qué buen gusto! El {c} se ve en todas partes. ¿Hay algo de ese color que te encante?"]
BOT_COLOR_V = ["¡Tenemos el mismo gusto! El violeta es mi color favorito también. ¿Qué te gusta de él?", "¡No te puedo creer, el violeta es el mío! Qué buena coincidencia."]
ASK_MY_COLOR = ["¿cuál es mi color favorito?", "¿qué color me gusta?", "¿te acordás de mi color favorito?"]
BOT_MY_COLOR = ["Tu color favorito es el {c}. ¡Lo tengo anotado en la memoria!", "Me dijiste que te gusta el {c}."]


def flow_color(rng, filler):
    c = rng.choice(COLORS)
    bot = rng.choice(BOT_COLOR_V) if c == "violeta" else rng.choice(BOT_COLOR).format(c=c)
    turns = [(rng.choice(SAY_COLOR).format(c=c), bot)]
    turns += _maybe_filler(rng, filler)
    if rng.random() < 0.5:
        turns.append((rng.choice(ASK_MY_COLOR), rng.choice(BOT_MY_COLOR).format(c=c)))
    return turns


# ------------------------------------------------------------------ edad
SAY_AGE = ["tengo {n} años", "tengo {n}", "cumplí {n} años", "tengo {n} años, ¿y vos?", "mi edad es {n}", "tengo {n} añitos", "voy a cumplir {n} años"]
BOT_AGE = ["¡{n} años! Una edad con mucho por vivir. ¿Qué es lo que más disfrutás de esta etapa?", "¡Qué bien, {n} años! Cada edad tiene su encanto. ¿Qué te gustaría hacer este año?", "¡{n}! Gracias por contarme. ¿Qué cosa te hace feliz últimamente?"]
ASK_MY_AGE = ["¿cuántos años tengo?", "¿te acordás de mi edad?", "¿qué edad tengo?", "¿sabés cuántos años tengo?"]
BOT_MY_AGE = ["Tenés {n} años, me lo dijiste hace un rato.", "Me contaste que tenés {n} años.", "Tu edad es {n}. ¡Memoria de IA chiquita!"]


def flow_age(rng, filler):
    n = rng.randint(10, 70)
    turns = [(rng.choice(SAY_AGE).format(n=n), rng.choice(BOT_AGE).format(n=n))]
    turns += _maybe_filler(rng, filler)
    if rng.random() < 0.55:
        turns.append((rng.choice(ASK_MY_AGE), rng.choice(BOT_MY_AGE).format(n=n)))
    return turns


# ------------------------------------------------------------------ mood que se recuerda
def flow_mood_memory(rng, filler):
    mood, bot_a, bot_b = rng.choice([
        ("triste", "Siento que estés pasando por esto. Acá estoy para escucharte. ¿Querés contarme qué pasó?", "Me dijiste que te sentías triste. ¿Cómo estás ahora, un poquito mejor?"),
        ("cansado", "Uf, el cansancio se siente. Si podés, tomate un rato para descansar. ¿Dormiste poco?", "Antes me dijiste que estabas cansado. ¿Pudiste descansar un poco?"),
        ("nervioso", "Es normal sentir nervios. Probá respirar hondo, inhalando cuatro segundos y soltando seis. ¿Qué es lo que viene?", "Antes estabas nervioso. ¿Cómo vas ahora, más tranquilo?"),
        ("contento", "¡Qué alegría! Me encanta que estés de buen humor. ¿Qué te tiene así?", "Me dijiste que estabas contento. ¿Seguís con esa buena energía?"),
    ])
    first = {"triste": ["estoy triste", "me siento triste", "hoy estoy muy triste"], "cansado": ["estoy cansado", "estoy muy cansado", "vengo agotado"],
             "nervioso": ["estoy nervioso", "estoy re nervioso", "tengo nervios"], "contento": ["estoy contento", "estoy re contento", "estoy feliz"]}[mood]
    turns = [(rng.choice(first), bot_a)]
    turns += _maybe_filler(rng, filler, 0.6)
    turns.append((rng.choice(["¿te acordás cómo estaba?", "¿cómo estaba yo?", "¿qué te dije antes?", "¿te acordás de lo que te dije?", "¿cómo me sentía?"]), bot_b))
    return turns


MEMORY_FLOWS = [("name", 9, flow_name), ("city", 4, flow_city), ("hobby", 4, flow_hobby), ("food", 4, flow_food), ("pet", 3, flow_pet),
                ("color", 2, flow_color), ("age", 2, flow_age), ("mood_mem", 2, flow_mood_memory)]

INTENTS = [
    I("bien_y_vos", ["bien, ¿y vos?", "bien y vos", "bien, ¿y tú?", "re bien, ¿y vos?", "todo bien, ¿y vos?", "genial, ¿y vos?", "muy bien, ¿y vos?", "bien y tú?", "excelente, ¿y vos?", "tranqui, ¿y vos?", "bien, gracias, ¿y vos?", "bien bien, ¿y vos qué tal?"],
      ["¡Qué bueno! Yo también estoy muy bien, con ganas de charlar. ¿Qué hiciste hoy?", "¡Me alegra! Yo, de diez: chiquita pero feliz. ¿Pasó algo lindo hoy?", "¡Genial, entonces estamos igual! Yo bien, gracias por preguntar. ¿De qué charlamos?"], w=3),
    I("mal_y_vos", ["mal, ¿y vos?", "más o menos, ¿y vos?", "regular, ¿y vos?", "no muy bien, ¿y vos?", "cansado, ¿y vos?", "así así, ¿y vos?", "ahí vamos, ¿y vos?", "mal, ¿y tú?"],
      ["Lamento que no andes bien. Yo estoy bien, gracias por preguntar. ¿Querés contarme qué te pasa?", "Ay, qué pena. Yo estoy bien, con ganas de acompañarte. ¿Qué te tiene así?", "Yo estoy bien, gracias. Pero me importa cómo estás vos. ¿Qué pasó?"], w=2),
    I("y_vos_generico", ["¿y vos?", "y vos", "¿y tú?", "¿vos qué decís?", "¿y a vos?", "¿y tú qué?", "¿y vos qué opinás?", "¿vos qué pensás?", "¿y vos qué hacés?", "¿y vos, kermesse?"],
      ["Yo soy una IA chiquita, así que mi vida es charlar con gente como vos. ¡Y me encanta! ¿Qué más querés contarme?", "Yo estoy bien y contenta de charlar. Ahora quiero saber más de vos. ¿Qué te gusta hacer?", "A mí me gusta jugar con las palabras y conocer gente nueva. ¿Y a vos qué te divierte?"], w=2),
    I("respuesta_generica", ["hace mucho", "hace poco", "un tiempito", "casi todos los días", "a veces", "depende", "me relaja", "es divertido", "me gusta mucho", "con mis amigos", "con mi familia", "solo", "sola", "en casa", "por la tarde", "por la noche", "desde chico", "desde chica", "no sé bien", "porque me gusta", "me hace bien", "mucho", "un poco", "bastante"],
      ["¡Qué bueno! Se nota que lo disfrutás. ¿Y qué más te gusta hacer?", "Ah, mirá vos. Gracias por contarme. ¿Querés que juguemos algo o seguimos charlando?", "Me gusta conocerte así, de a poco. ¿Qué otra cosa te apasiona?", "Interesante. Contame un poco más, que me gusta escucharte.", "Entiendo. Gracias por compartirlo. ¿Y qué es lo que más disfrutás de eso?"], w=4),
    I("por_que", ["¿por qué?", "porque sí", "¿y por qué?", "¿por qué no?", "¿por qué decís eso?", "¿por qué dices eso?", "¿cómo así?", "¿y eso?", "¿en serio por qué?"],
      ["Buena pregunta. A veces las cosas simplemente son así, y yo no tengo todas las respuestas. ¿Vos qué pensás?", "Uf, me pillaste. Soy chiquita y no siempre sé explicar el porqué. ¿Qué opinás vos?", "No tengo una razón muy sabia, la verdad. ¿Querés que cambiemos de tema?"], w=2),
    I("cuentame_mas", ["contame más", "seguí", "¿y después?", "¿qué más?", "algo más", "contame más cosas", "seguí contando", "decime más", "¿y qué más?", "más info", "continuá"],
      ["Me encantaría seguir, pero mi memoria es cortita y ya me quedé sin más datos. Mejor contame vos, ¿qué te gustaría saber?", "Hasta ahí llegué, soy chiquita. ¿Querés que probemos con otro tema o un juego?", "Eso es todo lo que sé, perdón. ¿Qué tal si me contás algo vos?"], w=2),
    I("volver_empezar", ["empecemos de nuevo", "cambiemos de tema", "hablemos de otra cosa", "otro tema", "cambiá de tema", "mejor hablemos de otra cosa", "quiero cambiar de tema", "dejemos esto", "olvidalo", "olvídalo", "no importa", "da igual"],
      ["Dale, cambiemos. ¿Querés un chiste, una adivinanza o charlar de algo tuyo?", "Listo, tema nuevo. ¿Qué te gustaría hacer: jugar, escuchar un dato curioso o simplemente conversar?", "Sin problema. Arranquemos de cero: ¿cómo estuvo tu semana?"], w=2),
]
