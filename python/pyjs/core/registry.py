"""
Function registry for exported Python callables.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Registry:
    def __init__(self) -> None:
        self._functions: dict[str, Callable[..., Any]] = {}

    def register(
        self,
        func: Callable[..., Any],
        name: str | None = None,
    ) -> Callable[..., Any]:
        export_name = name or func.__name__

        if export_name in self._functions:
            raise ValueError(
                f"Function '{export_name}' is already registered."
            )

        self._functions[export_name] = func

        return func

    def unregister(self, name: str) -> None:
        self._functions.pop(name, None)

    def get(self, name: str) -> Callable[..., Any]:
        if name not in self._functions:
            raise KeyError(f"Unknown function: {name}")

        return self._functions[name]

    def call(self, name: str, *args, **kwargs):
        return self.get(name)(*args, **kwargs)

    def exists(self, name: str) -> bool:
        return name in self._functions

    def names(self) -> list[str]:
        return list(self._functions.keys())

    def clear(self) -> None:
        self._functions.clear()
