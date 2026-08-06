"""
Codec registry.
"""

from __future__ import annotations

from .base import Codec
from .exceptions import UnsupportedCodecError


class CodecRegistry:

    def __init__(self):

        self._codecs: dict[str, Codec] = {}


    def register(
        self,
        codec: Codec,
    ) -> None:

        self._codecs[codec.name] = codec


    def unregister(
        self,
        name: str,
    ) -> None:

        self._codecs.pop(name, None)


    def get(
        self,
        name: str,
    ) -> Codec:

        codec = self._codecs.get(name)

        if codec is None:
            raise UnsupportedCodecError(
                f"Codec not found: {name}"
            )

        return codec


    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._codecs


    def names(self) -> tuple[str, ...]:

        return tuple(self._codecs.keys())


    def clear(self):

        self._codecs.clear()
