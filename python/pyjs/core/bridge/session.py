"""
Session management for Bridge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class Session:
    id: str = field(default_factory=lambda: str(uuid4()))

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: float = field(default_factory=time)

    connected: bool = False

    def connect(self) -> None:
        self.connected = True

    def disconnect(self) -> None:
        self.connected = False


class SessionManager:
    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def create(self) -> Session:
        session = Session()

        self._sessions[session.id] = session

        return session

    def add(self, session: Session) -> None:
        self._sessions[session.id] = session

    def get(self, session_id: str) -> Session:
        return self._sessions[session_id]

    def remove(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def exists(self, session_id: str) -> bool:
        return session_id in self._sessions

    def all(self) -> list[Session]:
        return list(self._sessions.values())

    def clear(self) -> None:
        self._sessions.clear()

    def count(self) -> int:
        return len(self._sessions)
