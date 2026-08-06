"""
bridge.transport.base

Transport abstraction layer.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable


MessageHandler = Callable[[dict[str, Any]], Awaitable[None]]


class Transport(ABC):
    """
    Base transport interface.

    Responsible only for sending
    and receiving raw messages.

    It does not know about:
    - Request
    - Response
    - Event
    - Routing
    """


    def __init__(self) -> None:

        self._handler: MessageHandler | None = None


    def on_message(
        self,
        handler: MessageHandler,
    ) -> None:

        self._handler = handler


    async def receive(
        self,
        message: dict[str, Any],
    ) -> None:

        if self._handler is not None:

            await self._handler(
                message
            )


    @abstractmethod
    async def send(
        self,
        message: dict[str, Any],
    ) -> None:
        raise NotImplementedError


    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError


    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
