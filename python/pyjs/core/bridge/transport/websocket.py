"""
bridge.transport.websocket

WebSocket transport implementation.
"""

from __future__ import annotations

import asyncio
import json
import websockets

from typing import Any

from .base import Transport


class WebSocketTransport(Transport):
    """
    WebSocket based transport.

    Supports:
    - Python server
    - Python client
    - JavaScript clients
    """


    def __init__(
        self,
        url: str | None = None,
        websocket=None,
    ) -> None:

        super().__init__()

        self.url = url

        self.websocket = websocket

        self._task: asyncio.Task | None = None


    async def connect(self) -> None:

        if self.websocket is None:

            if self.url is None:

                raise ValueError(
                    "URL required."
                )


            self.websocket = await websockets.connect(
                self.url
            )


        self._task = asyncio.create_task(
            self._receive_loop()
        )


    async def send(
        self,
        message: dict[str, Any],
    ) -> None:


        if self.websocket is None:

            raise RuntimeError(
                "WebSocket is not connected."
            )


        payload = json.dumps(
            message,
            ensure_ascii=False,
        )


        await self.websocket.send(
            payload
        )


    async def _receive_loop(self):

        async for message in self.websocket:

            data = json.loads(
                message
            )

            await self.receive(
                data
            )


    async def close(self):

        if self._task:

            self._task.cancel()


        if self.websocket:

            await self.websocket.close()


        self.websocket = None
