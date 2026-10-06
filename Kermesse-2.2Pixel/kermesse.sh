#!/usr/bin/env sh
# Lanzador para Linux / macOS / Termux:   sh kermesse.sh   (o:  sh kermesse.sh --lento)
cd "$(dirname "$0")/src" || exit 1
exec python3 chat.py "$@"
