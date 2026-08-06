"""
bridge/response.py

RPC response model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .packet import Packet


@dataclass(slots=True, kw_only=True)
class Response(Packet):
    """
    Represents a response to a Request.
    """

    type: str = "response"

    request_id: str

    success: bool = True

    result: Any = None

    error: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = super().to_dict()

        payload.update(
            {
                "request_id": self.request_id,
                "success": self.success,
                "result": self.result,
                "error": self.error,
            }
        )

        return payload

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Response":
        return cls(
            id=data["id"],
            protocol=data.get("protocol", "1.0"),
            timestamp=data["timestamp"],
            metadata=data.get("metadata", {}),
            request_id=data["request_id"],
            success=data.get("success", True),
            result=data.get("result"),
            error=data.get("error"),
        )

    @property
    def failed(self) -> bool:
        return not self.success

    @property
    def ok(self) -> bool:
        return self.success
