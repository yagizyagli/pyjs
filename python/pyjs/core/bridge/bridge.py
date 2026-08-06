"""
bridge.bridge

Main public Bridge API.
"""

from __future__ import annotations

from typing import Any, Callable, Awaitable

from protocol.event import Event

from .router import Router
from .dispatcher import Dispatcher
from .client import Client
from .server import Server
from .middleware import Middleware, MiddlewarePipeline


Transport = Callable[[dict[str, Any]], Awaitable[None]]


class Bridge:

    def __init__(
        self,
        transport: Transport | None = None,
    ) -> None:

        self.router = Router()

        self.dispatcher = Dispatcher(
            self.router
        )

        self.middleware = MiddlewarePipeline()

        self.client: Client | None = None

        self.server: Server | None = None


        if transport:

            self.client = Client(
                transport
            )

            self.server = Server(
                self.dispatcher,
                transport,
                self.middleware,
            )


    def expose(
        self,
        name: str,
        handler: Callable,
        namespace: str = "default",
    ):

        return self.router.register(
            name,
            handler,
            namespace,
        )


    def remove(
        self,
        name: str,
        namespace: str = "default",
    ):

        self.router.unregister(
            name,
            namespace,
        )


    def on(
        self,
        event: str,
        handler: Callable,
    ):

        self.router.on(
            event,
            handler,
        )


    def off(
        self,
        event: str,
        handler: Callable,
    ):

        self.router.off(
            event,
            handler,
        )


    def use(
        self,
        middleware: Middleware,
    ):

        self.middleware.add(
            middleware
        )


    async def call(
        self,
        method: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:

        if self.client is None:

            raise RuntimeError(
                "Client transport is not configured."
            )


        return await self.client.call(
            method,
            *args,
            **kwargs,
        )


    async def emit(
        self,
        name: str,
        data: Any = None,
    ):

        if self.client is None:

            raise RuntimeError(
                "Client transport is not configured."
            )


        await self.client.emit(
            name,
            data,
        )


    async def receive(
        self,
        packet,
    ):

        if self.server is None:

            raise RuntimeError(
                "Server transport is not configured."
            )


        await self.server.receive(
            packet
        )
