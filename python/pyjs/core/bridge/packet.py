"""
bridge/packet.py

Base packet model for the PyJS bridge protocol.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import monotonic
from typing import Any
from uuid import uuid4


@dataclass(slots=True, kw_only=True)
class Packet:
    """
    Base protocol packet.
    """

    id: str = field(default_factory=lambda: uuid4().hex)

    type: str

    protocol: str = "1.0"

    timestamp: float = field(default_factory=monotonic)

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "protocol": self.protocol,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Packet":
        return cls(
            id=data["id"],
            type=data["type"],
            protocol=data.get("protocol", "1.0"),
            timestamp=data.get("timestamp", monotonic()),
            metadata=data.get("metadata", {}),
        )
