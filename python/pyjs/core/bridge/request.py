"""
bridge/request.py

RPC request model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .packet import Packet


@dataclass(slots=True, kw_only=True)
class Request(Packet):
    """
    Represents a remote procedure call request.
    """

    type: str = "request"

    method: str

    args: tuple[Any, ...] = field(default_factory=tuple)

    kwargs: dict[str, Any] = field(default_factory=dict)

    timeout: float = 30.0

    expects_response: bool = True

    def to_dict(self) -> dict[str, Any]:
        payload = super().to_dict()

        payload.update(
            {
                "method": self.method,
                "args": list(self.args),
                "kwargs": self.kwargs,
                "timeout": self.timeout,
                "expects_response": self.expects_response,
            }
        )

        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Request":
        return cls(
            id=data["id"],
            protocol=data.get("protocol", "1.0"),
            timestamp=data["timestamp"],
            metadata=data.get("metadata", {}),
            method=data["method"],
            args=tuple(data.get("args", ())),
            kwargs=data.get("kwargs", {}),
            timeout=data.get("timeout", 30.0),
            expects_response=data.get("expects_response", True),
        )
