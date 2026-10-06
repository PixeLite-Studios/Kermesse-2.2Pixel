"""
Simula charlas completas con Kermesse y guarda las transcripciones (útil para ver cómo responde).
    python demo_chat.py  ->  escribe checkpoints/conversaciones.json  y  ejemplos_de_charla.md
"""
import json
import os
from generate import Kermesse, ROOT

GUIONES = {
    "Charla casual": ["hola", "bien y vos?", "estoy aburrido", "piedra papel o tijera", "papel"],
    "Conociéndose": ["¿cómo te llamás?", "me llamo Lucas", "¿cómo me llamo?", "¿sos una persona?", "¿cuántos parámetros tenés?", "¿tenés internet?"],
    "Juegos": ["contame un chiste", "jajaja", "adivinanza", "es pera", "piedra papel o tijera", "tijera"],
    "Un mal día": ["estoy muy triste", "me siento solo", "dame ánimo", "estoy nervioso por un examen"],
    "Datos y cuentas": ["¿cuál es la capital de Chile?", "¿y la de Colombia?", "¿cuánto es 8 por 7?", "¿cuánto es 15% de 80?", "mi hermana se llama Camila y tiene 30 años", "¿quién es Camila?", "¿qué edad tiene ella?"],
    "Escribiendo informal": ["ola q tal", "kien sos", "q haces", "cuéntame un chiste porfa", "grax"],
    "Lo que no sabe": ["¿quién ganó el mundial de 2022?", "¿qué hora es?", "¿cómo está el clima hoy?", "¿de qué sí podemos hablar?"],
}

if __name__ == "__main__":
    k = Kermesse(temperature=0.55, seed=2024, memory_path=None)
    todo, md = {}, ["# Charlas de ejemplo con Kermesse-2.2Pixel\n", "_Generadas por `src/demo_chat.py` con semilla fija; los datos personales de esta demostración no se guardan en disco._\n"]
    for titulo, lineas in GUIONES.items():
        k.reset()
        md.append(f"\n## {titulo}\n")
        todo[titulo] = []
        for u in lineas:
            r = k.reply(u)
            todo[titulo].append([u, r])
            md.append(f"**vos:** {u}  \n**kermesse:** {r}\n")
            print(f"vos: {u}\nkermesse: {r}\n", flush=True)
        print("-" * 60)
    json.dump(todo, open(os.path.join(ROOT, "checkpoints", "conversaciones.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(ROOT, "ejemplos_de_charla.md"), "w", encoding="utf-8").write("\n".join(md))
