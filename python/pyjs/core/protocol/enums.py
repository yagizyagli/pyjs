from __future__ import annotations

from enum import Enum


class PacketType(str, Enum):

    REQUEST = "request"

    RESPONSE = "response"

    EVENT = "event"

    ERROR = "error"

    HEARTBEAT = "heartbeat"


class PacketPriority(int, Enum):

    LOW = 10

    NORMAL = 50

    HIGH = 100

    CRITICAL = 255


class PacketStatus(str, Enum):

    CREATED = "created"

    SENT = "sent"

    RECEIVED = "received"

    PROCESSING = "processing"

    COMPLETED = "completed"

    FAILED = "failed"
