#!/bin/sh
# Оба параметра: --vfs и --script
cd "$(dirname "$0")/.." || exit 1
python3 -m src.emulator --vfs data/vfs.zip --script scripts/start_stage2.emu
echo "exit code: $?"
