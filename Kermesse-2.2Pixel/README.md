# Kermesse-2.2Pixel

Creada por **PixeLite**.

Asistente conversacional en español, para terminal y Termux. Funciona en el dispositivo, sin internet, servidor ni interfaz web. Conserva el Transformer de NumPy y añade una memoria local explícita, cálculo seguro y respuestas verificables.

## Modelo y entrenamiento

- **1.200.472 parámetros entrenables** (`d_model=128`, 6 capas, 4 cabezas, `d_ff=511`, contexto de 384 caracteres).
- Entrenado desde cero durante **35.000 pasos**, con AdamW y lotes pequeños para funcionar dentro del límite de memoria, sobre las **16.490 conversaciones** del conjunto de entrenamiento; las 510 conversaciones de validación quedan fuera del entrenamiento.
- Resultado final medido: pérdida **0,090** en las 510 conversaciones de validación; la suite fija de comportamiento pasó **200/200 casos**. Es una prueba acotada, no una garantía de conocimiento general.
- El checkpoint se guarda con el estado del optimizador. Si el proceso se interrumpe, reanudalo con `--resume`.
- El límite de carga y entrenamiento es **2.000.000 de parámetros**.

## Qué hace mejor

- Calcula expresiones aritméticas seguras con paréntesis, prioridad de operaciones, división, porcentajes, potencias y raíces cuadradas; entiende números escritos en español.
- Responde capitales guardadas y declara cuando no tiene un dato comprobado.
- Recuerda nombre, ciudad, edad, gustos, trabajo y relaciones explícitas; usa esas relaciones al contestar preguntas como «¿quién es Camila?».
- Puede conservar esos recuerdos entre ejecuciones en `data/user_memory.json`. El archivo queda en este dispositivo y no se transmite. `/memoria` muestra lo recordado y `/reset` lo borra junto con el historial.
- Conserva juegos, adivinanzas, chistes, respuestas empáticas y el modelo generativo como respaldo para la conversación abierta.
- Busca responder con calidez y contexto sin hacer pasar una suposición por un recuerdo o un dato.

Los recuerdos se guardan únicamente cuando Kermesse detecta una afirmación explícita (por ejemplo, «me llamo Lucía» o «mi hermana se llama Camila»). No hay sincronización ni llamadas de red.

## Requisitos y ejecución

Necesitás Python 3.9 o posterior y NumPy.

**Windows:** instalá NumPy con `py -m pip install numpy` y abrí `kermesse.bat`.

**macOS / Linux:**

```sh
python3 -m pip install numpy
sh kermesse.sh
```

**Termux (Android):**

```sh
pkg update && pkg install python python-numpy unzip
unzip Kermesse-2.2Pixel.zip
cd Kermesse-2.2Pixel
sh kermesse.sh
```

En Termux instalá NumPy con `python-numpy` desde `pkg`, no con `pip`. También podés ejecutar `python src/chat.py --lento` para ver la respuesta carácter por carácter.

## Comandos

- `/memoria`: muestra los recuerdos locales.
- `/reset`: borra historial y recuerdos guardados en el dispositivo.
- `/temp 0.5`: ajusta la creatividad del generador (de 0.05 a 2.0).
- `/ayuda` y `/salir`.

## Entrenar y verificar

Desde la carpeta `src`:

```sh
python train.py --steps 35000 --lr 0.002
python test_assistant_logic.py
python test_engine_ops.py
python eval_suite.py
```

`train.py` usa el corpus completo disponible y produce el checkpoint de `Kermesse-2.2Pixel`. Para continuar una ejecución interrumpida, agregá `--resume`. La evaluación incluida cubre 200 casos de cálculo, capitales, memoria, relaciones, juegos, identidad y conversación; es una prueba acotada, no una garantía de que el modelo resuelva cualquier tema.
