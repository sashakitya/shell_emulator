"""Вспомогательные функции для тестов."""

import contextlib
import io


def capture(func, *args, **kwargs):
    """Вызывает func и возвращает (результат, вывод в stdout)."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args, **kwargs)
    return result, buffer.getvalue()
