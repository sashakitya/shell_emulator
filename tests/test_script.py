"""Тесты этапа 2: параметры запуска и стартовые скрипты."""

import os
import tempfile
import unittest
from argparse import Namespace

from src.commands import ExitShell
from src.emulator import main, parse_args, print_config
from src.shell import Shell
from tests.helpers import capture


class ScriptTests(unittest.TestCase):
    """Проверки стартового скрипта и параметров запуска."""

    def setUp(self):
        """Готовит данные для каждого теста."""
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.folder = folder.name
        self.shell = Shell()

    def write_script(self, text):
        """Записывает скрипт во временный каталог и возвращает путь."""
        path = os.path.join(self.folder, "start.emu")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path

    def test_shows_input_and_output(self):
        path = self.write_script("# comment\n\ncd\n")
        ok, out = capture(self.shell.run_script, path)
        self.assertTrue(ok)
        self.assertIn("$ cd", out)

    def test_stops_on_first_error(self):
        path = self.write_script("cd\nzzz-unknown\ncd after\n")
        ok, out = capture(self.shell.run_script, path)
        self.assertFalse(ok)
        self.assertIn("error on line 2", out)
        self.assertNotIn("cd after", out)

    def test_missing_script(self):
        ok, out = capture(self.shell.run_script, "no-such.emu")
        self.assertFalse(ok)
        self.assertIn("Cannot read script", out)

    def test_exit_in_script(self):
        path = self.write_script("exit\n")
        with self.assertRaises(ExitShell):
            capture(self.shell.run_script, path)

    def test_parse_args(self):
        args = parse_args(["--vfs", "a.zip", "--script", "s.emu"])
        self.assertEqual((args.vfs, args.script), ("a.zip", "s.emu"))

    def test_print_config(self):
        _, out = capture(print_config, Namespace(vfs="a.zip", script=None))
        self.assertIn("[debug] vfs = a.zip", out)
        self.assertIn("[debug] script = (not set)", out)

    def test_main_runs_script(self):
        path = self.write_script("cd\nexit\n")
        code, out = capture(main, ["--script", path])
        self.assertEqual(code, 0)
        self.assertIn(f"[debug] script = {path}", out)

    def test_main_script_error(self):
        path = self.write_script("zzz-unknown\n")
        code, _ = capture(main, ["--script", path])
        self.assertEqual(code, 1)
