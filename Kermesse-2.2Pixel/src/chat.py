"""
Chat de terminal con Kermesse-2.2Pixel.

    python chat.py                  # charla normal
    python chat.py --lento          # escribe letra por letra
    python chat.py --temp 0.5       # más serena / 0.9 más creativa
    python chat.py --sin-color      # sin colores (también respeta NO_COLOR)
    python chat.py --demo           # charla de ejemplo automática

Comandos: /ayuda /info /guardar /memoria /reset /temp 0.7 /salir
"""
import argparse
import os
import shutil
import sys
import time
from datetime import datetime

try:
    import numpy  # noqa: F401
except ModuleNotFoundError:
    sys.exit("Falta NumPy. En Termux: pkg install python-numpy   (en otros sistemas: python3 -m pip install numpy)")

try:
    import readline  # historial con flechas ↑↓ (no existe en Windows)
except ImportError:
    readline = None

from generate import Kermesse, MODEL_NAME, VERSION, CREATOR, ROOT

COL = sys.stdout.isatty() and "NO_COLOR" not in os.environ

BANNER = r"""
  _  __                                          
 | |/ /___ _ __ _ __ ___   ___  ___ ___  ___     
 | ' // _ \ '__| '_ ` _ \ / _ \/ __/ __|/ _ \    
 | . \  __/ |  | | | | | |  __/\__ \__ \  __/    
 |_|\_\___|_|  |_| |_| |_|\___||___/___/\___|    
"""


def C(code, s):
    return f"\033[{code}m{s}\033[0m" if COL else s


def P(code, s):
    """Color para el prompt de input(): readline necesita marcar los códigos invisibles."""
    if not COL:
        return s
    if readline:
        return f"\001\033[{code}m\002{s}\001\033[0m\002"
    return f"\033[{code}m{s}\033[0m"


def banner():
    width = shutil.get_terminal_size((80, 24)).columns
    if width >= 52:
        print(C("95", BANNER))
    else:
        print(C("95", "\n  ✦ K E R M E S S E ✦"))
    print(C("95", f"  {MODEL_NAME}") + C("2", f" · por {CREATOR}"))


def ayuda():
    print(C("2", "  Comandos\n"
                 "   /info      versión, parámetros y estado\n"
                 "   /guardar   guarda esta charla en un .txt\n"
                 "   /memoria   muestra lo que recuerda (solo en tu dispositivo)\n"
                 "   /reset     borra historial y recuerdos\n"
                 "   /temp 0.5  creatividad (0.05 a 2.0)\n"
                 "   /salir     termina   ·   Ctrl+C cancela una respuesta\n\n"
                 "  Probá\n"
                 "   cuentas, capitales, chistes, adivinanzas, piedra-papel-tijera,\n"
                 "   contale tu nombre, ciudad o hobby, o preguntale quién la creó."))


def info(k, turnos):
    mem = "sí" if k.logic.memory_path else "no"
    print(C("2", f"  {MODEL_NAME} (v{VERSION}) · creada por {CREATOR}\n"
                 f"  {k.model.n_params():,} parámetros".replace(",", ".") +
                 f" · temperatura {k.temperature} · memoria en disco: {mem} · turnos: {turnos}"))


def guardar(log):
    if not log:
        print(C("2", "(todavía no hay nada que guardar)"))
        return
    carpeta = os.path.join(ROOT, "charlas")
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, datetime.now().strftime("charla_%Y%m%d_%H%M%S.txt"))
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(f"{MODEL_NAME} - charla del {datetime.now():%Y-%m-%d %H:%M}\n\n")
            for u, r in log:
                f.write(f"vos: {u}\nkermesse: {r}\n\n")
        print(C("2", f"(guardada en {os.path.relpath(ruta, ROOT)})"))
    except OSError as e:
        print(C("2", f"(no pude guardar: {e})"))


def responder(k, t, lento):
    """Muestra 'pensando…' hasta la primera letra; Ctrl+C cancela solo esta respuesta."""
    out = []
    gen = k.reply_stream(t)
    prompt = C("95", "kermesse > ")
    if COL:
        print(prompt + C("2", "pensando…"), end="", flush=True)
    else:
        print(prompt, end="", flush=True)
    try:
        for ch in gen:
            if not out and COL:
                print("\r\033[K" + prompt, end="")
            out.append(ch)
            print(C("95", ch), end="", flush=True)
            if lento:
                time.sleep(0.012)
    except KeyboardInterrupt:
        gen.close()
        if not out and COL:
            print("\r\033[K" + prompt, end="")
        print(C("2", " (respuesta cancelada)"))
        print()
        return None
    print("\n")
    return "".join(out).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--temp", type=float, default=0.6)
    ap.add_argument("--lento", action="store_true", help="escribe letra por letra")
    ap.add_argument("--sin-color", action="store_true", help="desactiva los colores")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()

    global COL
    if a.sin_color:
        COL = False

    k = Kermesse(temperature=a.temp, seed=a.seed, **({"memory_path": None} if a.demo else {}))
    banner()
    print(C("2", "  funciona localmente, sin internet · escribí /ayuda\n"))

    log = []
    demo = ["hola", "me llamo Sofía", "¿quién te creó?", "cuánto es 6 por 7", "¿cuál es la capital de Perú?", "¿cómo me llamo?", "chau"]
    while True:
        try:
            if a.demo:
                if not demo:
                    break
                text = demo.pop(0)
                print(C("96", "vos > ") + text)
            else:
                text = input(P("96", "vos > "))
        except (EOFError, KeyboardInterrupt):
            print()
            break
        t = text.strip()
        if t in ("/salir", "/exit", "/q"):
            break
        if t == "/reset":
            if not a.demo:
                try:
                    if input(P("93", "¿Borrar historial y recuerdos guardados? (s/n) ")).strip().lower() not in ("s", "si", "sí"):
                        print(C("2", "(cancelado)"))
                        continue
                except (EOFError, KeyboardInterrupt):
                    print()
                    continue
            k.reset(); log.clear(); print(C("2", "(memoria borrada)")); continue
        if t == "/memoria":
            if not k.logic.facts:
                print(C("2", "(no hay recuerdos locales guardados)"))
            else:
                extra = " (no pude guardarla en disco; seguirá disponible hasta salir)" if k.logic.memory_save_error else " (guardada solo en este dispositivo)"
                print(C("2", f"({k.logic.context_summary()}{extra})"))
            continue
        if t == "/info":
            info(k, len(log)); continue
        if t == "/guardar":
            guardar(log); continue
        if t.startswith("/temp"):
            try:
                value = float(t.split()[1])
                if not 0.05 <= value <= 2.0:
                    raise ValueError
                k.temperature = value
                print(C("2", f"(temperatura = {k.temperature})"))
            except Exception:
                print(C("2", "uso: /temp 0.7 (valor entre 0.05 y 2.0)"))
            continue
        if t == "/ayuda":
            ayuda(); continue
        if not t:
            continue
        resp = responder(k, t, a.lento)
        if resp is not None:
            log.append((t, resp))
    print(C("95", "kermesse > ") + "¡Hasta pronto! Volvé cuando quieras.")


if __name__ == "__main__":
    main()
