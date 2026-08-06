"""
bridge.server

RPC server implementation.
"""

from __future__ import annotations

from typing import Awaitable, Callable

from protocol.packet import Packet
from protocol.response import Response

from .dispatcher import Dispatcher
from .middleware import MiddlewarePipeline


Transport = Callable[[Packet], Awaitable[None]]


class Server:

    def __init__(
        self,
        dispatcher: Dispatcher,
        transport: Transport,
        middleware: MiddlewarePipeline | None = None,
    ) -> None:

        self.dispatcher = dispatcher

        self.transport = transport

        self.middleware = (
            middleware
            or MiddlewarePipeline()
        )

    async def receive(
        self,
        packet: Packet,
    ) -> None:

        async def process(
            value: Packet,
        ) -> None:

            result = await self.dispatcher.dispatch(
                value,
            )

            if isinstance(result, Response):

                await self.transport(result)

        await self.middleware.execute(
            packet,
            process,
        )

    async def shutdown(self) -> None:
        """
        Reserved for connection cleanup.
        """
        return None
