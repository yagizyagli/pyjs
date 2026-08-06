from typing import Any


class Context:
    """
    Shared state between Python and JavaScript.
    """

    def __init__(self):
        self._data: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def remove(self, key: str) -> None:
        self._data.pop(key, None)

    def clear(self) -> None:
        self._data.clear()

    def has(self, key: str) -> bool:
        return key in self._data

    def all(self) -> dict[str, Any]:
        return self._data.copy()
