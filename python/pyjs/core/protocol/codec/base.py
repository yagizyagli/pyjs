"""
protocol.codec.base

Codec abstraction layer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Codec(ABC):
    """
    Base interface for all serializers.
    """

    name: str = "base"

    content_type: str = "application/octet-stream"

    binary: bool = False

    @abstractmethod
    def encode(self, data: Any) -> bytes | str:
        """
        Serialize object.
        """
        raise NotImplementedError

    @abstractmethod
    def decode(self, payload: bytes | str) -> Any:
        """
        Deserialize object.
        """
        raise NotImplementedError

    def dumps(self, data: Any) -> bytes | str:
        return self.encode(data)

    def loads(self, payload: bytes | str) -> Any:
        return self.decode(payload)
