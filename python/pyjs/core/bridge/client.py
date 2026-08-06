"""
bridge.client

RPC client implementation.
"""

from __future__ import annotations

from typing import Any, Awaitable, Callable

from protocol.event import Event
from protocol.packet import Packet
from protocol.request import Request
from protocol.response import Response

from .futures import FutureManager
from .ids import generate_request_id


Transport = Callable[[Packet], Awaitable[None]]


class Client:

    def __init__(
        self,
        transport: Transport,
        futures: FutureManager | None = None,
    ) -> None:

        self.transport = transport

        self.futures = futures or FutureManager()

    async def call(
        self,
        method: str,
        *args: Any,
        timeout: float = 30.0,
        **kwargs: Any,
    ) -> Any:

        request_id = generate_request_id()

        request = Request(
            id=request_id,
            method=method,
            args=args,
            kwargs=kwargs,
            timeout=timeout,
        )

        pending = self.futures.create(
            request_id=request_id,
            method=method,
            timeout=timeout,
            metadata={},
        )

        await self.transport(request)

        return await pending.future

    async def emit(
        self,
        name: str,
        data: Any = None,
    ) -> None:

        event = Event(
            name=name,
            data=data,
        )

        await self.transport(event)

    def handle_response(
        self,
        response: Response,
    ) -> None:

        if response.success:

            self.futures.resolve(
                response.request_id,
                response.result,
            )

        else:

            self.futures.reject(
                response.request_id,
                Exception(response.error),
            )
