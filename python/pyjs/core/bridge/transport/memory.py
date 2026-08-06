"""
bridge.transport.memory

In-memory transport implementation.
"""

from __future__ import annotations

from typing import Any

from .base import Transport


class MemoryTransport(Transport):
    """
    Local memory based transport.

    Used for testing and internal communication.
    """


    def __init__(self) -> None:

        super().__init__()

        self._peer: MemoryTransport | None = None

        self._connected = False


    def connect_peer(
        self,
        peer: "MemoryTransport",
    ) -> None:

        self._peer = peer


    async def connect(self) -> None:

        self._connected = True


    async def send(
        self,
        message: dict[str, Any],
    ) -> None:


        if not self._connected:

            raise RuntimeError(
                "Transport is not connected."
            )


        if self._peer is None:

            raise RuntimeError(
                "No peer connected."
            )


        await self._peer.receive(
            message
        )


    async def close(self) -> None:

        self._connected = False

        self._peer = None
