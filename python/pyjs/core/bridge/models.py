from __future__ import annotations

from dataclasses import dataclass, field
from time import monotonic
from typing import Any
import asyncio


@dataclass(slots=True)
class PendingRequest:

    id: str

    method: str

    future: asyncio.Future[Any]

    created_at: float = field(default_factory=monotonic)

    timeout: float = 30.0

    metadata: dict[str, Any] = field(default_factory=dict)

    cancelled: bool = False

    completed: bool = False
