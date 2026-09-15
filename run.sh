#!/bin/sh
# Запуск эмулятора из любого каталога: ./run.sh [параметры]
PYTHONPATH="$(dirname "$0")" python3 -m src.emulator "$@"
