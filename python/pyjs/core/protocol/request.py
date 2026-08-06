"""
protocol.request

RPC request packet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .enums import PacketType
from .packet import Packet


@dataclass(slots=True, kw_only=True)
class Request(Packet):

    type: PacketType = PacketType.REQUEST

    method: str

    args: tuple[Any, ...] = field(default_factory=tuple)

    kwargs: dict[str, Any] = field(default_factory=dict)

    timeout: float = 30.0

    def to_dict(self) -> dict[str, Any]:

        data = super().to_dict()

        data.update(
            {
                "method": self.method,
                "args": list(self.args),
                "kwargs": self.kwargs,
                "timeout": self.timeout,
            }
        )

        return data

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "Request":

        return cls(
            id=data["id"],
            protocol=data["protocol"],
            version=data["version"],
            magic=data["magic"],
            timestamp=data["timestamp"],
            priority=data["priority"],
            status=data["status"],
            metadata=data.get("metadata", {}),
            extensions=data.get("extensions", {}),
            method=data["method"],
            args=tuple(data.get("args", [])),
            kwargs=data.get("kwargs", {}),
            timeout=data.get("timeout", 30.0),
        )
