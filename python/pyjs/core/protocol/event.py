"""
protocol/event.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .packet import Packet
from .enums import PacketType


@dataclass(slots=True, kw_only=True)
class Event(Packet):
    """
    One-way event packet.

    Events never expect a response.
    """

    type: PacketType = PacketType.EVENT

    name: str

    data: Any = None

    broadcast: bool = False

    channel: str = "default"

    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        packet = super().to_dict()

        packet.update(
            {
                "name": self.name,
                "data": self.data,
                "broadcast": self.broadcast,
                "channel": self.channel,
                "tags": self.tags,
            }
        )

        return packet

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Event":
        return cls(
            id=payload["id"],
            protocol=payload["protocol"],
            version=payload["version"],
            magic=payload["magic"],
            timestamp=payload["timestamp"],
            priority=payload["priority"],
            status=payload["status"],
            metadata=payload.get("metadata", {}),
            extensions=payload.get("extensions", {}),
            name=payload["name"],
            data=payload.get("data"),
            broadcast=payload.get("broadcast", False),
            channel=payload.get("channel", "default"),
            tags=payload.get("tags", []),
        )
