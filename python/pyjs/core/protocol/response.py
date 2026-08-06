"""
protocol.response

RPC response packet.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .enums import PacketType
from .packet import Packet


@dataclass(slots=True, kw_only=True)
class Response(Packet):

    type: PacketType = PacketType.RESPONSE

    request_id: str

    success: bool

    result: Any = None

    error: Any = None

    def to_dict(self) -> dict[str, Any]:

        data = super().to_dict()

        data.update(
            {
                "request_id": self.request_id,
                "success": self.success,
                "result": self.result,
                "error": self.error,
            }
        )

        return data

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "Response":

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
            request_id=data["request_id"],
            success=data["success"],
            result=data.get("result"),
            error=data.get("error"),
        )
