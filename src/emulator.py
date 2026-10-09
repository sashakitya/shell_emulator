"""Точка входа эмулятора оболочки UNIX-подобной ОС."""
import argparse
import sys

from src.commands import ExitShell
from src.shell import Shell

EXIT_OK = 0
EXIT_ERROR = 1
NOT_SET = "(not set)"


def parse_args(argv):
    """Разбирает параметры командной строки."""
    parser = argparse.ArgumentParser(
        prog="emulator",
        description="Эмулятор оболочки UNIX-подобной ОС.",
    )
    parser.add_argument("--vfs", help="путь к физическому расположению VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args(argv)


def print_config(args):
    """Отладочный вывод всех заданных параметров запуска."""
    for key, value in sorted(vars(args).items()):
        shown = NOT_SET if value is None else value
        print(f"[debug] {key} = {shown}")


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


def run(args):
    """Выполняет стартовый скрипт (если задан) и запускает REPL."""
    shell = Shell()
    try:
        if args.script and not shell.run_script(args.script):
            return EXIT_ERROR
        repl(shell)
    except ExitShell:
        pass
    return EXIT_OK


def main(argv=None):
    """Разбирает параметры, выводит их и запускает эмулятор."""
    args = parse_args(argv)
    print_config(args)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
