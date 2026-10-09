#!/bin/sh
# Запуск без параметров (VFS по умолчанию), команды берутся из stdin
cd "$(dirname "$0")/.." || exit 1
echo exit | python3 -m src.emulator
echo "exit code: $?"
