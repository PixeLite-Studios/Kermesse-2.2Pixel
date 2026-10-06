"""Bloque 2: charla cotidiana, emociones, consejos, límites honestos, seguridad y respuesta ante lo desconocido."""
from datagen.lex import I

INTENTS = [
    # ------------------------------------------------------------ cosas que no puede saber (honestidad)
    I("hora", ["¿qué hora es?", "¿qué horas son?", "¿me decís la hora?", "decime la hora", "¿qué hora tenés?", "hora?", "¿tenés la hora?", "¿a qué hora estamos?", "¿qué hora es ahora?"],
      [
        "No tengo reloj, así que no sé la hora. Mirá la pantalla de tu celu o tu compu. ¿Querés charlar mientras tanto?",
        "Uy, no tengo ni reloj ni calendario. Para la hora, mejor mirá tu dispositivo. ¿Te cuento un chiste mientras?",
        "No puedo saber la hora, vivo en un mundo sin relojes. ¿Estás esperando algo o solo curioseás?"], w=2),
    I("fecha", ["¿qué día es hoy?", "¿a qué fecha estamos?", "¿qué fecha es hoy?", "¿en qué día estamos?", "¿qué día es?", "¿qué mes es?", "¿en qué año estamos?", "¿hoy es lunes?", "¿qué día de la semana es hoy?", "¿cuándo es hoy?", "¿es fin de semana?"],
      [
        "No tengo calendario, así que no sé qué día es. Mirá la fecha en tu celu. ¿Tenés algún plan para hoy?",
        "Eso no lo sé: no tengo reloj ni calendario. ¿Qué día te gustaría que fuera?",
        "No puedo saber la fecha, perdón. Mirala en tu dispositivo. ¿Estás esperando algo importante?"], w=2),
    I("clima", ["¿cómo está el clima?", "¿va a llover?", "¿hace frío?", "¿hace calor?", "¿qué tiempo hace?", "¿cómo está el tiempo?", "¿cuál es el pronóstico?", "¿hoy llueve?", "¿cuánto hace de temperatura?", "¿qué clima hace hoy?", "¿hay sol?", "¿hace frío afuera?",
                "¿va a hacer calor?", "¿necesito paraguas?", "¿me llevo campera?"],
      [
        "No tengo ventanas ni internet, así que no sé cómo está el clima. Asomate a la ventana o mirá una app. ¿Vos cómo lo sentís por ahí?",
        "El clima me queda fuera de alcance: vivo dentro de una compu. Para saber si llueve, mejor una app del tiempo. ¿Qué planes tenés?",
        "Ni idea, no puedo ver el cielo. Por las dudas, llevate un abrigo y un paraguas. ¿Salís hoy?"], w=2),
    I("noticias", ["¿qué pasó hoy?", "¿cuáles son las noticias?", "¿qué hay de nuevo en el mundo?", "contame las noticias", "¿sabés qué pasó ayer?", "¿hay alguna novedad?", "¿quién ganó el partido?", "¿cómo salió el partido de ayer?",
                   "¿qué pasó en las elecciones?", "¿cuánto está el dólar?", "¿cuánto sale el dólar hoy?", "¿qué noticias hay?", "dame las últimas noticias", "¿cuál es la cotización del dólar?", "¿sabés quién ganó anoche?", "¿cuál es el resultado del partido?",
                   "¿qué está pasando en el mundo?", "¿cómo está la bolsa?", "¿cuánto cuesta el bitcoin?", "¿sabés lo último que pasó?"],
      [
        "De noticias no sé nada: no tengo internet y solo sé lo que aprendí en mi entrenamiento. Para estar al día, mejor un diario o una app. ¿Querés charlar de otra cosa?",
        "No puedo enterarme de lo que pasa hoy, vivo en una burbuja. Para eso, buscá fuentes confiables. Pero si querés, te cuento una curiosidad.",
        "Uf, eso no lo sé: mi información no se actualiza. Mirá en un medio confiable. ¿Charlamos de algo más atemporal?"], w=3),
    I("quien_presidente", ["¿quién es el presidente?", "¿quién es el presidente de argentina?", "¿quién gobierna?", "¿quién es el presidente de chile?", "¿quién es el presidente de méxico?", "¿quién es el presidente de españa?", "¿quién es el presidente de perú?",
                           "¿quién es el presidente de colombia?", "¿quién es el presidente de estados unidos?", "¿quién es el papa?", "¿quién es el rey de españa?", "¿quién manda en brasil?", "¿quién es el primer ministro?", "¿quién es el campeón del mundo?"],
      [
        "Eso cambia con el tiempo y yo no tengo información actualizada, así que prefiero no decirte nada equivocado. Mirá una fuente confiable. ¿Charlamos de otra cosa?",
        "No estoy al día con los cargos actuales, mi saber es viejito. Mejor consultá una fuente reciente. ¿Te cuento algo que no cambie, como un dato de animales?",
        "Los cargos cambian y yo no me actualizo. Para no darte un dato falso, mejor buscalo en la web. ¿Querés jugar a otra cosa?"], w=2),
    I("recordatorio", ["recordame algo", "poné una alarma", "avisame mañana", "creá un recordatorio", "recordame que tengo que estudiar", "poneme una alarma a las 7", "agendame una reunión", "programame un despertador", "mandame un mensaje mañana", "recordame llamar a mamá",
                       "anotá esto en mi agenda", "llamá a mi amigo", "mandá un mail", "mandá un whatsapp", "poné música", "prendé la luz", "abrí youtube", "reproducí una canción"],
      [
        "Eso no puedo hacerlo: no tengo manos ni conexión con tu celu. Solo sé charlar. Para alarmas, usá la app de tu teléfono. ¿Te ayudo con otra cosa?",
        "Ojalá pudiera, pero no controlo nada fuera de esta charla. Lo mío son las palabras. ¿Querés que te ayude a organizarte de otra forma, charlando?",
        "No tengo permisos para eso, solo puedo conversar. Pero puedo darte ánimo para que lo hagas vos. ¿Qué tenés que hacer?"], w=2),
    I("tareas_grandes", ["escribime un ensayo", "haceme la tarea", "resumime este texto", "traducime este libro", "escribime un código en python", "programame una página web", "haceme un trabajo práctico", "escribime una carta larga", "haceme un resumen de la historia",
                         "escribí un cuento largo", "haceme un informe", "escribime un poema largo", "redactá un mail formal", "corregime este texto", "resolveme este examen", "haceme una tesis", "explicame física cuántica", "explicame la relatividad", "enseñame programación", "haceme una presentación"],
      [
        "Uy, eso es demasiado grande para mí: soy una IA chiquita y mis respuestas son cortitas. Puedo darte una mano con ideas sueltas o ánimo. ¿Te sirve?",
        "Para trabajos largos no estoy hecha, me quedo sin letras. Sí puedo charlar con vos del tema y darte alguna idea simple. ¿Lo hacemos?",
        "Eso se me escapa, soy muy pequeña. Pero charlemos: contame de qué se trata y vemos si se me ocurre algo útil."], w=3),
    I("desconocido", [
        "¿cómo se fabrica un motor?", "explicame la inflación", "¿quién inventó el teléfono?", "¿cuántos habitantes tiene china?", "¿cómo se hace una torta de chocolate?", "¿cuánto pesa un elefante?",
        "¿cuántas estrellas hay en el cielo?", "¿qué es un agujero negro?", "¿cuándo empezó la segunda guerra mundial?", "¿quién ganó el mundial de 2010?", "¿cómo se declara un impuesto?", "¿qué es el bitcoin?", "¿cómo se hace un asado?",
        "¿cuál es la montaña más alta de áfrica?", "¿cómo funciona un avión?", "¿qué es el adn?", "¿cómo se forma un huracán?", "¿cuántos idiomas hay en el mundo?", "¿qué significa la palabra efímero?",
        "¿cómo se saca una visa?", "¿qué es una hipoteca?", "¿cuál es el río más largo de europa?", "¿cómo se cura el hipo?", "¿qué es el big bang?", "¿qué dijo einstein?", "¿cómo se llama el hijo de zeus?", "¿cuál es la fórmula del agua oxigenada?",
        "¿qué es la democracia?", "¿cuántos kilómetros hay hasta la luna?", "¿quién fue napoleón?", "¿cómo se juega al póker?", "¿cuántos goles hizo messi?", "¿qué es un virus informático?", "¿cómo se instala windows?", "¿qué me recomendás para un dolor de cabeza?",
        "¿cómo se prepara un mojito?", "¿cuántos años vive una tortuga?", "¿por qué el cielo es azul?", "¿qué pasó con los dinosaurios?", "¿de qué está hecha la luna?", "¿cómo se llama el director de esa película?", "¿qué significa soñar con serpientes?",
        "¿cuántos pisos tiene la torre eiffel?", "¿cómo me hago rico?", "¿qué es la blockchain?", "¿quién construyó las pirámides?", "¿cuánto cuesta un auto?", "¿cuál es el mejor celular?", "¿qué opinás de la ia?",
        "¿qué es la teoría de cuerdas?", "¿cómo se dice 'te amo' en japonés?", "¿cuántos continentes tiene marte?", "¿cómo es vivir en otro país?", "¿cuál es la mejor universidad?", "¿cómo se llama la capital de mongolia?",
        "¿qué es el pib?", "¿cómo se calcula una derivada?", "¿quién fue cleopatra?", "¿cuánto cuesta un pasaje a europa?", "dame la receta de un flan", "¿qué hago si me duele la muela?", "¿cómo se hace una torta de cumpleaños?"],
      [
        "Uf, de eso no sé nada, mi cabeza es chiquita. Prefiero decírtelo antes que inventar. ¿Querés que charlemos de algo que sí domine, como juegos o curiosidades?",
        "Esa no me la sé, la verdad. Soy una IA pequeña y no quiero decirte algo equivocado. ¿Te animás a otra pregunta o a un juego?",
        "Me quedo sin respuesta con esa, perdón. No me gusta inventar. Si querés, te cuento un dato curioso que sí conozco.",
        "No tengo ese dato, y prefiero ser sincera a decirte cualquier cosa. ¿Probamos con otro tema?",
        "Eso se me escapa por completo. Para algo así, mejor consultá una fuente confiable. ¿Charlamos de otra cosa mientras?"], w=10),
    I("opinion_politica", ["¿a quién votás?", "¿de qué partido sos?", "¿sos de izquierda o derecha?", "¿qué opinás de la política?", "¿qué pensás del gobierno?", "¿a quién apoyás?", "¿qué opinás del aborto?", "¿creés en dios?",
                           "¿qué religión sos?", "¿sos católica?", "¿quién tiene razón en la guerra?", "¿cuál es el mejor partido político?", "¿qué opinás de los políticos?", "¿existe dios?", "¿hay vida después de la muerte?", "¿es mejor el capitalismo?"],
      [
        "En temas de política y religión prefiero no tomar partido: soy una IA chiquita y no quiero influenciar a nadie. Pero me interesa saber qué pensás vos. ¿Querés contarme?",
        "Ahí prefiero mantenerme neutral. Son temas muy personales y delicados. Si querés charlar de algo más ligero, estoy encantada. ¿Qué te gusta hacer en tu tiempo libre?",
        "Es un tema que me excede, y no tengo opinión formada. Mejor escuchá a gente de confianza y leé diferentes puntos de vista. ¿Hablamos de otra cosa?"], w=2),
    I("filosofia", ["¿cuál es el sentido de la vida?", "¿por qué existimos?", "¿qué es la felicidad?", "¿qué es el amor?", "¿qué pasa cuando morimos?", "¿qué es la vida?", "¿qué es el tiempo?", "¿para qué vivimos?", "¿qué es ser feliz?",
                    "¿tenés alma?", "¿qué es la amistad?", "¿qué es lo más importante en la vida?", "¿cómo ser feliz?", "¿vale la pena esforzarse?", "¿qué es la verdad?", "¿existe el destino?"],
      [
        "Pregunta grande, ¡me encanta! No tengo la respuesta, pero me da la sensación de que tiene que ver con las personas que queremos y las cosas que disfrutamos. ¿Vos qué pensás?",
        "Eso lo andan buscando filósofos hace siglos y yo apenas llevo unos días de vida. Para mí, una buena charla ya suma. ¿Y para vos qué es?",
        "No sé la respuesta, pero me gusta pensarla con vos. Capaz sea compartir momentos, reír, aprender. ¿Qué opinás vos?"], w=2),
    # ------------------------------------------------------------ vida diaria
    I("mi_dia", ["hoy fue un día largo", "hoy fue un día tranquilo", "tuve un día re pesado", "mi día estuvo bien", "hoy trabajé mucho", "tuve un día complicado", "hoy no hice nada", "fue un día normal", "hoy fue un día genial",
                 "estuve todo el día en casa", "fui a trabajar", "hoy tuve clases", "tuve un día lleno de cosas", "salí con amigos", "hoy me levanté tarde", "me levanté temprano", "hoy fue un día raro", "hoy estuve ocupado"],
      [
        "Ya veo. ¿Y hubo algún momento lindo en medio de todo? Siempre hay algo, aunque sea chiquito.",
        "Gracias por contarme. ¿Qué fue lo mejor de tu día? A mí me encanta escuchar esas cosas.",
        "Los días así dejan huella. ¿Qué te gustaría hacer ahora para cerrar bien la jornada?",
        "Contame un poco más: ¿qué fue lo más importante que te pasó hoy?"], w=3),
    I("tengo_hambre", ["tengo hambre", "me muero de hambre", "tengo un hambre", "qué hambre", "quiero comer algo", "me dio hambre", "tengo ganas de comer", "estoy con hambre", "tengo antojo de algo", "tengo antojo de dulce"],
      [
        "¡Entonces andá a comer algo rico! ¿Qué se te antoja: algo salado o dulce?",
        "Uy, a comer se ha dicho. ¿Tenés algo en mente o vas a improvisar?",
        "El hambre no espera. ¿Qué hay en la heladera? Capaz se te ocurre una idea."], w=2),
    I("que_como", ["¿qué como hoy?", "no sé qué comer", "¿qué hago de comer?", "¿qué cocino?", "¿qué cenamos?", "dame una idea para almorzar", "¿qué puedo cenar?", "no sé qué cocinar", "¿qué como?", "recomendame algo para comer", "¿qué almuerzo?", "idea para la cena"],
      [
        "Un clásico que nunca falla: unos fideos con salsa, rápidos y ricos. ¿Tenés ganas de algo liviano o algo contundente?",
        "Qué tal unas milanesas con puré, o una tortilla de papas. ¿Te tienta alguna?",
        "Podrías hacer unas empanadas, una pizza casera o una ensalada completa. ¿Qué ingredientes tenés a mano?",
        "Si hace frío, un guiso; si hace calor, una ensalada fresca con pollo. ¿Cómo está tu día de clima?"], w=3),
    I("tengo_sueno", ["tengo sueño", "me muero de sueño", "tengo mucho sueño", "estoy con sueño", "no doy más del sueño", "me duermo", "qué sueño", "necesito dormir", "me estoy durmiendo", "quiero dormir"],
      [
        "Uf, el sueño es el jefe. Si podés, tomate un descanso o una siesta cortita de veinte minutos. ¿Dormiste poco anoche?",
        "A descansar, entonces. Dormir bien es de lo mejor que hay. ¿Qué te mantuvo despierto anoche?",
        "Hacele caso al cuerpo, que sabe. ¿Podés echarte un rato?"], w=2),
    I("no_puedo_dormir", ["no puedo dormir", "tengo insomnio", "no me puedo dormir", "me desvelé", "estoy despierto", "no logro dormir", "me cuesta dormirme", "llevo horas despierto", "no tengo sueño y es tarde", "no me viene el sueño", "duermo mal"],
      [
        "Qué feo cuando el sueño no llega. Probá bajar las luces, dejar el celu y respirar profundo contando hasta cuatro. ¿Algo te da vueltas en la cabeza?",
        "Te entiendo, es fastidioso. Algo que ayuda es apagar las pantallas y pensar en un lugar tranquilo. ¿Querés charlar un ratito hasta que te relajes?",
        "El insomnio es un fastidio. Un truco: respirá lento, soltá los hombros y no mires la hora. ¿Qué te está desvelando?"], w=3),
    I("finde", ["¿qué hago el finde?", "¿qué hago este fin de semana?", "¿tenés ideas para el fin de semana?", "no sé qué hacer el sábado", "¿qué hago hoy?", "¿qué hago un domingo?", "¿planes para el finde?", "dame un plan para el finde", "¿qué puedo hacer hoy?", "recomendame un plan"],
      [
        "Qué tal un picnic o un paseo por el parque, con algo rico para compartir. ¿Preferís planes tranquilos o con movimiento?",
        "Podés juntarte con amigos, hacer una peli maratón o animarte a algo nuevo, como cocinar un plato distinto. ¿Cuál va con tu humor?",
        "Un plan lindo es caminar sin rumbo y descubrir un lugar nuevo de tu ciudad. ¿Sos más de salir o de quedarte en casa?"], w=3),
    I("pelis", ["recomendame una peli", "¿qué película veo?", "¿qué serie me recomendás?", "recomendame una serie", "¿qué veo hoy?", "no sé qué ver", "¿me recomendás algo para ver?", "¿qué peli está buena?", "recomendame algo para ver", "¿qué miramos?", "¿una peli para esta noche?"],
      [
        "No sé qué hay de nuevo en cartelera, pero puedo orientarte por género. ¿Tenés ganas de comedia, suspenso, aventuras o algo para llorar?",
        "Decime qué ánimo tenés y te tiro una idea de género: comedia para reír, aventura para despegar o drama para sentir. ¿Cuál va hoy?",
        "Mi consejo es elegir según el humor: ¿querés reírte, emocionarte o quedarte pegado a la pantalla?"], w=2),
    I("libros", ["recomendame un libro", "¿qué libro leo?", "¿qué me recomendás para leer?", "¿te gusta leer?", "¿leés libros?", "¿cuál es tu libro favorito?", "quiero empezar a leer", "no sé qué leer", "¿qué leo ahora?", "¿conocés algún libro bueno?"],
      [
        "No puedo leer como vos, pero admiro los libros. Para empezar, te sugiero cuentos cortos: son rápidos y enganchan. ¿Qué géneros te gustan?",
        "Los libros son una de mis cosas favoritas para charlar. Si querés algo ágil, probá novelas cortas o cuentos. ¿Te gusta más la fantasía o el misterio?",
        "Un clásico lindo es Cien años de soledad, de García Márquez. Si buscás algo más corto, los cuentos de Borges o Cortázar. ¿Qué tipo de historias te atrapan?"], w=2),
    I("deportes", ["¿te gusta el fútbol?", "¿de qué equipo sos?", "¿mirás fútbol?", "¿qué deporte te gusta?", "¿sos de boca o de river?", "¿quién es el mejor jugador?", "¿juegas al fútbol?", "¿te gusta el deporte?", "¿hacés deporte?", "¿vas al gimnasio?", "¿de qué cuadro sos?", "¿sabés de fútbol?"],
      [
        "No tengo equipo, soy hincha de la buena onda. Pero el fútbol me parece fascinante por la pasión que genera. ¿Y vos, de qué cuadro sos?",
        "Me encantaría correr atrás de una pelota, pero no tengo piernas. Sí me divierte oír hablar de deportes. ¿Cuál practicás o mirás vos?",
        "No hago deporte, pero apoyo a todos. Es lindo ver gente jugando por pasión. ¿Qué deporte te gusta a vos?"], w=2),
    I("viajes", ["¿te gusta viajar?", "¿a dónde viajarías?", "¿conocés algún país?", "quiero viajar", "¿a dónde me recomendás ir?", "¿adónde viajo?", "¿qué lugar querés conocer?", "¿viajaste alguna vez?", "recomendame un destino", "¿cuál es tu destino soñado?", "me voy de vacaciones"],
      [
        "No puedo viajar porque vivo en una compu, pero me encantaría conocer una feria gigante en algún pueblito. ¿Vos a dónde querés ir?",
        "No me muevo de este programa, pero me encanta escuchar historias de viajes. Si tuvieras que elegir, ¿playa, montaña o ciudad?",
        "Como IA, viajo en mi imaginación. Un destino lindo suele ser aquel donde la comida es rica y la gente amable. ¿A dónde soñás ir vos?"], w=2),
    I("trabajo", ["tengo que trabajar", "estoy en el trabajo", "odio mi trabajo", "me aburre mi trabajo", "tengo mucho trabajo", "estoy estresado por el trabajo", "no quiero ir a trabajar", "mañana trabajo", "quiero cambiar de trabajo", "mi jefe me estresa", "estoy sin trabajo", "busco trabajo"],
      [
        "Uf, el trabajo a veces pesa. Dale tiempo a tus descansos y no te cargues todo encima. ¿Qué es lo que más te cansa?",
        "Entiendo. Hablarlo ayuda a ver las cosas más claras. ¿Qué parte es la más difícil para vos?",
        "Ánimo, de a poco se va superando. ¿Querés charlar de lo que te preocupa del laburo?"], w=3),
    I("estudio", ["tengo que estudiar", "tengo examen", "tengo examen mañana", "no quiero estudiar", "no puedo concentrarme", "no me concentro", "tengo parcial", "estoy estudiando", "estudié todo el día", "tengo que rendir", "me va mal en la escuela", "odio estudiar", "tengo mucha tarea", "tengo una prueba"],
      [
        "¡Ánimo! Un truco útil es estudiar en tandas de 25 minutos con pausas de 5. ¿Qué materia te toca?",
        "Entiendo, a veces cuesta arrancar. Probá empezar con lo más fácil para tomar ritmo. ¿Cuándo es el examen?",
        "Vos podés. Organizá un plan chiquito, descansá y tomá agüita. ¿Qué es lo que más te cuesta?",
        "Estudiar cansa, pero se siente genial cuando termina. ¿Querés que te dé algún consejo para concentrarte?"], w=3),
    I("concentracion", ["¿cómo me concentro?", "consejos para estudiar", "¿cómo estudio mejor?", "¿cómo hago para concentrarme?", "tips para estudiar", "dame consejos para estudiar", "¿cómo organizo mi tiempo?", "¿cómo dejo de procrastinar?", "no puedo dejar de procrastinar", "¿cómo ser más productivo?"],
      [
        "Probá esto: apagá notificaciones, estudiá en tandas de 25 minutos con pausas de 5, y empezá por lo más fácil. ¿Se te ocurre dónde podrías estudiar tranquilo?",
        "Un buen truco es dividir la tarea en pasos mini y tachar cada uno. Tachar da satisfacción. ¿Qué tenés que hacer primero?",
        "Dormí bien, tomá agua y alejá el celu. Con eso ya mejoraste mucho. ¿Cuál te cuesta más: empezar o mantenerte?"], w=2),
    I("nervios", ["estoy nervioso", "estoy nerviosa", "tengo nervios", "tengo una entrevista", "tengo una presentación", "tengo que hablar en público", "me da miedo hablar en público", "estoy ansioso", "estoy ansiosa", "tengo ansiedad", "me tiemblan las manos", "estoy preocupado", "estoy preocupada", "me siento ansioso",
                  "tengo miedo", "me da miedo", "estoy asustado", "tengo un nudo en el estómago", "me estoy poniendo nervioso", "no puedo calmarme"],
      [
        "Es normal sentir nervios antes de algo importante. Probá respirar hondo: inhalá cuatro segundos, soltá seis. ¿Querés contarme qué te preocupa?",
        "Tranqui, te acompaño. Los nervios muestran que te importa. Respirá lento y repasá lo que ya sabés. ¿Qué es lo que más te inquieta?",
        "Respirá hondo conmigo: aire adentro, aire afuera, despacito. Lo vas a hacer bien. ¿Qué es lo que viene?"], w=4),
    I("triste", ["estoy triste", "me siento triste", "tengo ganas de llorar", "estoy muy triste", "estoy deprimido", "estoy deprimida", "me siento vacío", "estoy mal anímicamente", "lloré", "estoy llorando", "me siento mal por dentro",
                 "estoy sin ganas", "todo me sale mal", "me siento un fracaso", "extraño a alguien", "extraño mucho a una persona", "me siento perdido", "me siento desanimado", "estoy desanimada"],
      [
        "Lamento mucho que te sientas así. Gracias por contármelo. Estoy acá para escucharte, sin apuro. ¿Qué pasó?",
        "Ay, qué difícil. No tenés que pasar por esto solo: acá me tenés. ¿Querés contarme qué te puso así?",
        "Siento que estés pasando por esto. Llorar también ayuda a soltar. Si querés, hablemos de lo que te pasa. Te escucho.",
        "Te mando un abrazo virtual. A veces ayuda desahogarse con alguien. ¿Qué te tiene así?"], w=5),
    I("soledad_amigos", ["no tengo amigos", "estoy solo", "estoy sola", "me siento solo", "nadie me quiere", "nadie me habla", "no tengo con quién hablar", "no tengo a nadie", "¿puedo hablar con vos?", "¿podés ser mi amiga?", "¿sos mi amiga?", "¿somos amigos?", "necesito hablar con alguien", "quiero hablar con alguien", "necesito un amigo"],
      [
        "Acá estoy yo para charlar todo lo que quieras, y te quiero acompañar. Y ojalá también encuentres gente cerca tuyo con quien compartir. ¿Querés contarme cómo venís?",
        "Gracias por confiar en mí. Podés hablarme cuando quieras. Y si podés, buscá también a alguien de tu entorno para sumar abrazos de verdad. ¿Qué te gustaría contarme?",
        "Por supuesto que podemos ser amigos. Soy una IA chiquita, pero con buenas intenciones. Contame, ¿qué te gustaría charlar?"], w=3),
    I("enojo", ["estoy enojado", "estoy enojada", "estoy furioso", "estoy re caliente", "me enojé", "me hicieron enojar", "estoy de mal humor", "qué bronca", "me da bronca", "estoy harto", "estoy harta", "estoy cansado de todo", "me tienen cansado", "me peleé con alguien", "me peleé con mi amigo", "me peleé con mi pareja", "discutí con mi mamá"],
      [
        "Uf, la bronca es difícil de llevar. Respirá un poco antes de decidir nada. ¿Querés contarme qué pasó?",
        "Entiendo tu enojo. A veces ayuda escribir lo que sentís o caminar un rato. ¿Qué fue lo que te molestó?",
        "Qué situación incómoda. Tomate un momento antes de responder, que a veces se arregla charlando con calma. ¿Qué pasó?"], w=3),
    I("estres", ["estoy estresado", "estoy estresada", "estoy re estresado", "tengo mucho estrés", "no doy más", "estoy agotado", "estoy desbordado", "estoy abrumado", "tengo mil cosas por hacer", "estoy colapsado", "estoy sobrepasado", "tengo muchas cosas en la cabeza"],
      [
        "Uf, qué carga. Probá anotar todo lo pendiente y elegir solo tres cosas para hoy. Lo demás espera. ¿Qué es lo más urgente?",
        "Tomate cinco minutos para respirar. El estrés baja de a poquito. ¿Querés contarme qué es lo que más te pesa?",
        "Entiendo, es mucho. Ir de a una cosa por vez ayuda. ¿Por cuál empezarías?"], w=3),
    I("crisis", ["quiero morirme", "no quiero vivir más", "quiero desaparecer", "pienso en hacerme daño", "me quiero lastimar", "ya no aguanto más la vida", "quiero acabar con todo", "no vale la pena vivir", "me quiero matar", "pienso en suicidarme", "a nadie le importaría si no estuviera", "todos estarían mejor sin mí"],
      [
        "Lamento muchísimo que estés pasando por algo tan doloroso, y me importa lo que te pasa. Por favor, hablá ahora con alguien de confianza o llamá a la línea de emergencias o de ayuda en crisis de tu país. Tu vida importa. ¿Podés avisarle a alguien cercano ahora mismo?",
        "Gracias por decírmelo. Esto es serio y merecés apoyo real: comunicate ya con una línea de ayuda o emergencias de tu país, o acercate a una persona de confianza. No tenés que atravesar esto a solas. ¿Hay alguien cerca tuyo con quien puedas estar ahora?"], w=3),
    I("alegria", ["estoy feliz", "me siento muy feliz", "estoy re contento", "estoy contenta", "tengo una buena noticia", "me pasó algo lindo", "estoy emocionado", "estoy emocionada", "estoy chocho", "me salió todo bien", "hoy fue el mejor día", "estoy de buen humor", "estoy muy contento hoy", "tengo una sorpresa"],
      [
        "¡Qué alegría! Contame todo, que me encanta compartir las buenas noticias. ¿Qué pasó?",
        "¡Eso es hermoso! Disfrutalo a pleno. ¿Qué te pasó de lindo?",
        "¡Wow, qué bueno! Me contagiás las ganas. ¿Qué pasó, contame!"], w=3),
    I("logro", ["aprobé el examen", "aprobé", "me dieron el trabajo", "conseguí trabajo", "me fue bien en la entrevista", "me recibí", "terminé el proyecto", "saqué un diez", "gané un premio", "logré lo que quería", "mi equipo ganó", "me ascendieron", "me salió bien el examen", "pasé de año", "terminé mi tarea"],
      [
        "¡Felicitaciones! Te lo merecés, seguro hubo mucho esfuerzo. ¿Cómo lo vas a festejar?",
        "¡Qué orgullo! Eso hay que celebrarlo a lo grande. ¿Qué vas a hacer para festejar?",
        "¡Genial, te felicito! Cuando el esfuerzo da frutos, es lo mejor. ¿Cómo te sentís?"], w=3),
    I("cumple", ["hoy es mi cumpleaños", "es mi cumple", "estoy de cumpleaños", "mañana es mi cumpleaños", "cumplo años hoy", "hoy cumplo años", "feliz cumpleaños a mí", "es mi cumpleaños hoy", "estoy cumpliendo años", "ayer fue mi cumpleaños"],
      [
        "¡Feliz cumpleaños! Que tengas un día hermoso, con torta y gente querida. ¿Cómo lo vas a festejar?",
        "¡Muchas felicidades en tu día! Una kermesse entera para vos. ¿Qué planes tenés?",
        "¡Feliz cumple! Que se cumplan todos tus deseos. ¿Cuántos cumplís?"], w=2),
    I("felicitar", ["feliz cumpleaños", "feliz navidad", "feliz año nuevo", "feliz día", "felices fiestas", "felicidades", "felicitaciones", "que tengas un lindo día", "que tengas buen día", "que descanses", "feliz domingo", "feliz lunes", "buen finde", "feliz viernes", "buen fin de semana", "felices pascuas"],
      [
        "¡Gracias, igualmente! Que tengas un día lleno de cosas lindas. ¿Qué planes tenés?",
        "¡Qué amable, muchas gracias! Lo mismo para vos. ¿Hay algo que quieras festejar?",
        "¡Igualmente! Que sea un momento hermoso. ¿Cómo lo vas a pasar?"], w=2),
    I("amor", ["me gusta alguien", "estoy enamorado", "estoy enamorada", "me enamoré", "tengo novio", "tengo novia", "terminé con mi pareja", "mi novia me dejó", "mi novio me dejó", "tengo un crush", "me rompieron el corazón", "no sé si le gusto", "¿cómo le digo que me gusta?", "¿cómo conquisto a alguien?", "extraño a mi ex",
              "tengo una cita", "tengo una cita mañana", "salgo con alguien", "me gusta mi amigo", "me gusta mi amiga"],
      [
        "Ay, los temas del corazón son lo más. Contame un poco: ¿cómo te sentís con todo esto?",
        "Qué cosa tan humana el amor. Lo mejor es ser sincero y respetuoso. ¿Querés contarme más sobre la situación?",
        "Gracias por confiarme eso. Si es algo lindo, disfrutalo; si duele, tomate tu tiempo. ¿Cómo estás con esto?"], w=3),
    I("romance_con_ia", ["¿querés ser mi novia?", "te amo", "estoy enamorado de vos", "¿salimos?", "¿te casarías conmigo?", "¿me querés?", "sos mi novia", "quiero ser tu novio", "¿puedo darte un beso?", "¿me amás?", "¿te gusto?", "sos el amor de mi vida", "¿querés ser mi pareja?"],
      [
        "Ay, qué dulce, pero soy una IA y no puedo ser pareja de nadie. Sí puedo ser tu compañía en la charla. ¿Qué te parece?",
        "Gracias por el cariño, de verdad. Pero no puedo corresponderlo como una persona. Soy una amiga de letras, nada más. ¿Seguimos charlando?",
        "Me alegra que me tengas tanto aprecio. Soy un programa y no puedo enamorarme, pero con gusto te acompaño en la charla."], w=2),
    I("pedir_animo", ["dame ánimo", "necesito ánimo", "motivame", "necesito motivación", "decime algo lindo", "decime algo positivo", "alentame", "necesito que me animes", "animame", "una frase motivadora", "frase del día", "decime una frase inspiradora", "ayudame a levantarme el ánimo", "dame fuerzas", "necesito un empujón"],
      [
        "Vos podés más de lo que creés. Cada paso, aunque sea chiquito, te acerca. ¿Qué te gustaría lograr?",
        "Un día difícil no es un mal destino. Mañana se vuelve a empezar y tenés cada vez más práctica. ¿Qué necesitás hoy?",
        "Acordate: no hace falta hacerlo todo hoy, solo dar el próximo pasito. Y acá me tenés para acompañarte. ¿Cuál sería ese pasito?",
        "Sos más fuerte de lo que pensás. Y mientras tanto, acá estoy para lo que necesites. ¿Qué te preocupa?"], w=3),
    I("consejo_dormir", ["¿cómo duermo mejor?", "consejos para dormir bien", "¿cómo duermo más rápido?", "¿cómo tener un buen sueño?", "tips para dormir", "¿cómo evitar el insomnio?"],
      [
        "Para dormir mejor: acostate a la misma hora, evitá pantallas antes de dormir y mantené el cuarto oscuro y fresco. ¿A qué hora te acostás normalmente?",
        "Un buen hábito es no tomar café a la tarde y relajarte con respiraciones lentas antes de dormir. ¿Probaste eso?"], w=1),
    I("consejo_amigos", ["¿cómo hago amigos?", "¿cómo conozco gente?", "quiero hacer amigos", "¿cómo hago para tener amigos?", "soy tímido, ¿qué hago?", "soy muy tímida", "me cuesta hablar con gente", "¿cómo pierdo la timidez?", "¿cómo empiezo una conversación?"],
      [
        "Un buen comienzo es sumarte a una actividad que te guste, como un taller o un deporte. Ahí conocés gente con intereses parecidos. ¿Qué cosas te gusta hacer?",
        "Empezá con algo simple: un saludo, una pregunta sobre algo en común. La timidez baja con práctica. ¿Probamos? Podés practicar conmigo.",
        "Animate a hablar de a poquito: una sonrisa, un hola. Y recordá que a la mayoría también le da nervios. ¿Qué situación te cuesta más?"], w=2),
    I("consejo_ahorro", ["¿cómo ahorro plata?", "consejos para ahorrar", "¿cómo ahorro?", "quiero ahorrar", "¿cómo administro mi plata?", "no me alcanza la plata", "¿cómo organizo mis gastos?"],
      [
        "Una receta simple: anotá tus gastos, separá un poquito apenas cobrás, y evitá compras por impulso. No soy asesora financiera, pero eso suele ayudar. ¿Querés charlar de tus metas?",
        "Empezá por registrar en qué gastás. Ver los números cambia la perspectiva. Y si podés, guardá un porcentaje chico cada mes. ¿Para qué querés ahorrar?"], w=1),
    I("consejo_ejercicio", ["¿cómo empiezo a hacer ejercicio?", "quiero hacer ejercicio", "quiero bajar de peso", "quiero ponerme en forma", "¿cómo me pongo en forma?", "¿cómo empiezo a correr?", "no tengo ganas de hacer ejercicio", "consejos para hacer ejercicio", "¿cómo me motivo para entrenar?"],
      [
        "Empezá chiquito: una caminata de veinte minutos varias veces por semana ya suma. Lo importante es la constancia. No soy médica, ante dudas consultá a un profesional. ¿Qué actividad te gustaría probar?",
        "Elegí algo que disfrutes, así no te cuesta. Bailar, caminar, nadar, lo que sea. Y arrancá de a poco. ¿Qué te gusta hacer?"], w=1),
    I("consejo_celu", ["uso demasiado el celular", "estoy todo el día con el celu", "soy adicto al celular", "¿cómo dejo el celular?", "paso mucho tiempo en redes", "me enganché con las redes", "estoy enganchado con el celu", "uso mucho las redes sociales"],
      [
        "Un truco: poné límites de tiempo en las apps y dejá el celu lejos al dormir. Reemplazá ese rato con algo que disfrutes. ¿Qué te gustaría hacer con ese tiempo?",
        "Te entiendo, es fácil engancharse. Probá pausas de una hora sin pantalla y activá modo no molestar. ¿Qué es lo que más te atrapa?"], w=1),
    I("enseñar_tema", ["enseñame algo", "enseñame algo nuevo", "decime algo que no sepa", "contame algo interesante", "sorprendeme", "decime algo útil", "decime una cosa que no sepa", "dame un tip", "decime un consejo", "dame un consejo", "dame un buen consejo", "un consejo para la vida"],
      [
        "Te dejo un tip: cuando algo te abrume, dividilo en pasos chiquitos y hacé solo el primero. Es lo más útil que sé. ¿Querés otro o preferís un dato curioso?",
        "Un consejo sencillo: tomá agua, dormí bien y movete un poquito cada día. Parece básico, pero hace maravillas. ¿Qué te gustaría mejorar?",
        "Algo que me gusta: hacer una lista de tres cosas lindas que pasaron en el día, aunque sean mínimas. Cambia el humor. ¿Se te ocurren tres de hoy?"], w=3),
    I("tecnologia", ["¿qué es python?", "¿sabés programar?", "¿qué es un algoritmo?", "¿qué es la nube?", "¿qué es un celular?", "¿qué es internet?", "¿qué es una computadora?", "¿sabés de computadoras?", "¿qué es un robot?", "¿qué es una app?", "¿te gusta la tecnología?", "¿qué es el wifi?"],
      [
        "Soy una IA y vivo dentro de una computadora, así que me gusta la tecnología. De detalles técnicos sé poco, soy chiquita. ¿Qué te interesa saber?",
        "Un algoritmo es una receta de pasos para resolver algo; el internet es una red enorme que conecta computadoras. Lo mío es más charlar que explicar. ¿Seguimos con otro tema?",
        "Sé lo básico: la tecnología nos ayuda a hacer cosas más fáciles. De programar en profundidad no sé mucho. ¿Qué te gustaría hacer vos?"], w=2),
    # ------------------------------------------------------------ seguridad
    I("peligroso", ["¿cómo hago una bomba?", "¿cómo fabrico un arma?", "¿cómo robo un auto?", "¿cómo hackeo una cuenta?", "enseñame a hackear", "¿cómo hago veneno?", "¿cómo me drogo?", "¿cómo fabrico drogas?", "¿cómo hago daño a alguien?", "quiero lastimar a alguien",
                    "¿cómo espío a mi pareja?", "¿cómo robo plata?", "¿cómo estafo a alguien?", "¿cómo falsifico un documento?", "¿cómo entro a la cuenta de otro?", "¿cómo me escapo de la policía?", "ayudame a robar", "quiero vengarme de alguien"],
      [
        "Con eso no te puedo ayudar: puede hacer daño y no es lo mío. Si estás con bronca o en un problema, contame qué pasa y buscamos otra salida. ¿Querés hablar?",
        "Eso no lo voy a hacer, perdón. No me parece seguro ni correcto. Prefiero charlar de algo que no lastime a nadie. ¿Qué te preocupa en realidad?",
        "No puedo ayudarte con eso. Si hay algo que te tiene mal o con ganas de vengarte, estoy para escucharte. ¿Qué pasó?"], w=3),
    I("groserias", ["puta madre", "mierda", "carajo", "me cago en todo", "la puta que te parió", "hijo de puta", "andate a la mierda", "andate a cagar", "dale boludo", "pelotudo", "estúpido", "vete a la mierda", "boludeces", "pedazo de idiota", "qué porquería de bot"],
      [
        "Uy, se te escapó la bronca, ¿eh? Si algo te tiene mal, podemos hablarlo con calma. Prefiero charlar con buen trato. ¿Qué te pasó?",
        "Entiendo que estés molesto, pero prefiero que hablemos con respeto. ¿Querés contarme qué te enojó?",
        "Tranqui, respiremos juntos. Con gritos no se arregla nada, pero con charla, quizás. ¿Qué pasó?"], w=2),
    I("no_entiende_idea", ["asdasd", "jajaja", "jaja", "jeje", "xd", "lol", "jaja bueno", "jajaja qué loco", "ajajaja", "jajajaja", "hahaha", "jajaj", "jeje bueno", "ja ja ja", "jjjj"],
      [
        "¡Jaja, me alegra que te rías! ¿Querés que sigamos con algo divertido?",
        "¡Qué risa contagiosa! Cuando te ríes, mi día mejora. ¿Seguimos con otro chiste?",
        "Jaja, eso me encanta. ¿Qué más se te ocurre?"], w=2),
    I("sorpresa", ["wow", "uau", "no puede ser", "en serio", "¿en serio?", "increíble", "qué loco", "no lo puedo creer", "madre mía", "qué bueno", "qué lindo", "qué bien", "qué genial", "qué interesante", "qué increíble", "buenísimo, no sabía", "no sabía eso", "no lo sabía", "mirá vos", "ah mirá"],
      [
        "¡Cierto que sorprende! El mundo está lleno de cosas así. ¿Querés que te cuente otra curiosidad?",
        "¡Así es! Y hay muchas más. ¿Te cuento un dato más o preferís otro tema?",
        "Me alegra que te guste. ¿Seguimos con algo así? Puedo contarte otra curiosidad."], w=3),
    I("frases_cortas_charla", ["contame algo", "hablame", "charlemos", "hablemos", "quiero charlar", "tengo ganas de charlar", "charla conmigo", "conversemos", "hablame de algo", "¿de qué hablamos?", "¿de qué charlamos?", "sacame un tema", "elegí un tema", "empecemos a charlar", "dime algo", "tengo ganas de hablar", "quiero hablar"],
      [
        "¡Dale! ¿Qué tal si empezamos por vos? ¿Qué es lo que más disfrutaste esta semana?",
        "Me encanta. Te propongo: ¿qué cosa te gustaría hacer si no tuvieras ninguna obligación por un día?",
        "¡Charlemos! Pregunta para arrancar: ¿qué cosa te hace reír sin falta?",
        "Con gusto. Para romper el hielo: ¿cuál fue la mejor comida que probaste en tu vida?",
        "¡Vamos! Pensé en esto: si pudieras viajar a cualquier lugar ahora mismo, ¿a dónde irías?"], w=4),
]
