#!/bin/sh
# Ошибка в стартовом скрипте и отсутствующий скрипт: код возврата 1
cd "$(dirname "$0")/.." || exit 1
python3 -m src.emulator --script scripts/start_error.emu
echo "exit code: $?"
python3 -m src.emulator --script scripts/no-such-script.emu
echo "exit code: $?"
