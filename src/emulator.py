"""Точка входа эмулятора оболочки UNIX-подобной ОС."""
import sys

from src.commands import ExitShell
from src.shell import Shell

EXIT_OK = 0


def repl(shell):
    """Читает и выполняет команды до exit или конца ввода (EOF).

    Если ввод идёт не с клавиатуры (канал), команды дублируются на
    экран, чтобы вывод выглядел как диалог.
    """
    while True:
        try:
            line = input(shell.prompt())
        except EOFError:
            print()
            return
        except KeyboardInterrupt:
            print()
            continue
        if not sys.stdin.isatty():
            print(line)
        try:
            shell.execute(line)
        except ExitShell:
            return


def main():
    """Запускает эмулятор."""
    repl(Shell())
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
