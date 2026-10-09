#!/bin/sh
# Параметр --vfs: путь к VFS (на этапе 2 только выводится)
cd "$(dirname "$0")/.." || exit 1
echo exit | python3 -m src.emulator --vfs data/vfs.zip
echo "exit code: $?"
