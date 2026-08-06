"""
bridge.bridge

Main Bridge API.
"""

from __future__ import annotations

from typing import Any, Callable

from ..protocol.codec import JSONCodec
from ..protocol.parser import PacketParser

from .client import Client
from .connection import Connection
from .dispatcher import Dispatcher
from .middleware import Middleware, MiddlewarePipeline
from .router import Router
from .server import Server
from .transport.base import Transport


class Bridge:

    def __init__(
        self,
        transport: Transport,
    ) -> None:

        self.router = Router()

        self.dispatcher = Dispatcher(
            self.router,
        )

        self.middleware = MiddlewarePipeline()

        self.parser = PacketParser(
            JSONCodec(),
        )

        #
        # Connection önce oluşturulur.
        #

        self.connection = Connection(
            transport=transport,
            parser=self.parser,
        )

        #
        # Client artık Connection üzerinden gönderir.
        #

        self.client = Client(
            self.connection.send,
        )

        self.server = Server(
            dispatcher=self.dispatcher,
            transport=self.connection.send,
            middleware=self.middleware,
        )

        #
        # Connection'a sonradan bağlanırlar.
        #

        self.connection.client = self.client
        self.connection.server = self.server

    async def start(self) -> None:
        await self.connection.start()

    async def stop(self) -> None:
        await self.connection.close()

    def expose(
        self,
        name: str,
        handler: Callable[..., Any],
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
    ) -> None:
        self.router.unregister(
            name,
            namespace,
        )

    def on(
        self,
        event: str,
        handler: Callable[..., Any],
    ) -> None:
        self.router.on(
            event,
            handler,
        )

    def off(
        self,
        event: str,
        handler: Callable[..., Any],
    ) -> None:
        self.router.off(
            event,
            handler,
        )

    def use(
        self,
        middleware: Middleware,
    ) -> None:
        self.middleware.add(
            middleware,
        )

    async def call(
        self,
        method: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return await self.client.call(
            method,
            *args,
            **kwargs,
        )

    async def emit(
        self,
        event: str,
        data: Any = None,
    ) -> None:
        await self.client.emit(
            event,
            data,
        )
