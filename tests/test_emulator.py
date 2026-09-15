"""Тесты этапа 1: парсер, приглашение, команды и REPL."""

import unittest
from unittest import mock

from src.commands import ExitShell
from src.emulator import repl
from src.shell import Shell, parse
from tests.helpers import capture


class ParseTests(unittest.TestCase):
    """Проверки разбора ввода."""

    def test_splits_command_and_args(self):
        self.assertEqual(parse("ls -l /tmp"), ("ls", ["-l", "/tmp"]))

    def test_empty_line(self):
        self.assertEqual(parse("   "), (None, []))


class ShellTests(unittest.TestCase):
    """Проверки выполнения команд."""

    def setUp(self):
        """Готовит данные для каждого теста."""
        self.shell = Shell()

    def test_prompt_format(self):
        prompt = self.shell.prompt()
        self.assertIn("@", prompt)
        self.assertTrue(prompt.endswith(":~$ "))

    def test_ls_stub(self):
        ok, out = capture(self.shell.execute, "ls -l")
        self.assertTrue(ok)
        self.assertEqual(out, "ls ['-l']\n")

    def test_cd_stub(self):
        ok, out = capture(self.shell.execute, "cd /tmp")
        self.assertTrue(ok)
        self.assertEqual(out, "cd ['/tmp']\n")

    def test_cd_too_many_args(self):
        ok, out = capture(self.shell.execute, "cd a b")
        self.assertFalse(ok)
        self.assertIn("cd: too many arguments", out)

    def test_unknown_command(self):
        ok, out = capture(self.shell.execute, "zzz-unknown")
        self.assertFalse(ok)
        self.assertIn("zzz-unknown: command not found", out)

    def test_empty_line_is_ok(self):
        ok, out = capture(self.shell.execute, "   ")
        self.assertTrue(ok)
        self.assertEqual(out, "")

    def test_exit(self):
        with self.assertRaises(ExitShell):
            self.shell.execute("exit")

    def test_exit_with_args(self):
        ok, out = capture(self.shell.execute, "exit 1")
        self.assertFalse(ok)
        self.assertIn("exit: too many arguments", out)


class ReplTests(unittest.TestCase):
    """Проверки цикла REPL."""

    def test_stops_on_exit(self):
        inputs = ["cd a b", "exit", "zzz-unknown"]
        with mock.patch("builtins.input", side_effect=inputs):
            _, out = capture(repl, Shell())
        self.assertIn("cd: too many arguments", out)
        self.assertNotIn("zzz-unknown", out)

    def test_stops_on_eof(self):
        with mock.patch("builtins.input", side_effect=EOFError):
            capture(repl, Shell())
