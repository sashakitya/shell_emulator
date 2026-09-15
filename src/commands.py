"""Команды эмулятора."""

MAX_CD_ARGS = 1


class CommandError(Exception):
    """Ошибка выполнения команды; текст показывается пользователю."""


class ExitShell(Exception):
    """Сигнал о завершении работы эмулятора."""


def cmd_ls(shell, args):
    """Заглушка ls: выводит имя команды и аргументы."""
    print("ls", args)


def cmd_cd(shell, args):
    """Заглушка cd: выводит имя команды и аргументы."""
    if len(args) > MAX_CD_ARGS:
        raise CommandError("too many arguments")
    print("cd", args)


def cmd_exit(shell, args):
    """Завершает работу эмулятора."""
    if args:
        raise CommandError("too many arguments")
    raise ExitShell()


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}
