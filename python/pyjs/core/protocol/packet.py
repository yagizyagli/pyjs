"""
protocol/packet.py

Base protocol packet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Any
from uuid import uuid4

from .enums import PacketPriority, PacketStatus, PacketType
from .exceptions import InvalidVersionError
from .version import (
    PROTOCOL_MAGIC,
    PROTOCOL_NAME,
    PROTOCOL_VERSION,
    SUPPORTED_VERSIONS,
)


@dataclass(slots=True, kw_only=True)
class Packet:
    """
    Base class for every protocol message.
    """

    id: str = field(default_factory=lambda: uuid4().hex)

    type: PacketType

    protocol: str = PROTOCOL_NAME

    version: str = PROTOCOL_VERSION

    magic: str = PROTOCOL_MAGIC

    timestamp: float = field(default_factory=time)

    priority: PacketPriority = PacketPriority.NORMAL

    status: PacketStatus = PacketStatus.CREATED

    metadata: dict[str, Any] = field(default_factory=dict)

    extensions: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if self.version not in SUPPORTED_VERSIONS:
            raise InvalidVersionError(
                f"Unsupported protocol version: {self.version}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "protocol": self.protocol,
            "version": self.version,
            "magic": self.magic,
            "timestamp": self.timestamp,
            "priority": self.priority.value,
            "status": self.status.value,
            "metadata": self.metadata,
            "extensions": self.extensions,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Packet":
        return cls(
            id=data["id"],
            type=PacketType(data["type"]),
            protocol=data.get("protocol", PROTOCOL_NAME),
            version=data.get("version", PROTOCOL_VERSION),
            magic=data.get("magic", PROTOCOL_MAGIC),
            timestamp=data.get("timestamp", time()),
            priority=PacketPriority(data.get("priority", PacketPriority.NORMAL.value)),
            status=PacketStatus(data.get("status", PacketStatus.CREATED.value)),
            metadata=data.get("metadata", {}),
            extensions=data.get("extensions", {}),
        )

    def copy(self, **changes: Any) -> "Packet":
        data = self.to_dict()
        data.update(changes)
        return self.from_dict(data)

    def set_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def set_extension(self, key: str, value: Any) -> None:
        self.extensions[key] = value

    def get_extension(self, key: str, default: Any = None) -> Any:
        return self.extensions.get(key, default)
