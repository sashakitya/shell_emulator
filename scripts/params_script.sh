#!/bin/sh
# Параметр --script: стартовый скрипт без ошибок
cd "$(dirname "$0")/.." || exit 1
python3 -m src.emulator --script scripts/start_stage2.emu
echo "exit code: $?"
