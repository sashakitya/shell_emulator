"""Ядро эмулятора: разбор ввода, выполнение команд и скриптов."""

import getpass
import socket

from src.commands import COMMANDS, CommandError

HOME_MARK = "~"
SEP = "/"


def parse(line):
    """Делит строку на команду и аргументы по пробелам.

    Возвращает кортеж (команда, список аргументов).
    Для пустой строки возвращает (None, []).
    """
    parts = line.split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


class Shell:
    """Состояние эмулятора и выполнение команд."""

    def __init__(self):
        """Создаёт оболочку с текущим каталогом в корне."""
        self.cwd = []

    def prompt(self):
        """Формирует приглашение вида username@hostname:~$ из данных ОС."""
        user = getpass.getuser()
        host = socket.gethostname()
        path = SEP + SEP.join(self.cwd) if self.cwd else HOME_MARK
        return f"{user}@{host}:{path}$ "

    def execute(self, line):
        """Выполняет строку ввода; возвращает False при ошибке команды."""
        command, args = parse(line)
        if command is None:
            return True
        handler = COMMANDS.get(command)
        if handler is None:
            print(f"{command}: command not found")
            return False
        try:
            handler(self, args)
        except CommandError as error:
            print(f"{command}: {error}")
            return False
        return True

    def run_script(self, path):
        """Выполняет стартовый скрипт, показывая и ввод, и вывод.

        Пустые строки и строки, начинающиеся с #, пропускаются.
        Выполнение останавливается на первой ошибке (возвращает False).
        """
        try:
            with open(path, encoding="utf-8") as handle:
                lines = handle.read().splitlines()
        except (OSError, UnicodeDecodeError):
            print(f"Cannot read script: {path}")
            return False
        for number, line in enumerate(lines, start=1):
            text = line.strip()
            if not text or text.startswith("#"):
                continue
            print(self.prompt() + text)
            if not self.execute(text):
                print(f"Script stopped: error on line {number}")
                return False
        return True
