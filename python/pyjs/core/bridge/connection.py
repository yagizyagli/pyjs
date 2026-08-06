"""
bridge.connection

Transport and protocol connection manager.
"""

from __future__ import annotations

from typing import Any

from protocol.packet import Packet
from protocol.response import Response
from protocol.parser import PacketParser

from .client import Client
from .server import Server
from .transport.base import Transport


class Connection:

    def __init__(
        self,
        transport: Transport,
        parser: PacketParser,
        client: Client | None = None,
        server: Server | None = None,
    ) -> None:

        self.transport = transport

        self.parser = parser

        self.client = client

        self.server = server


        self.transport.on_message(
            self._on_message
        )


    async def start(self) -> None:

        await self.transport.connect()


    async def send(
        self,
        packet: Packet,
    ) -> None:

        payload = self.parser.encode(
            packet
        )

        await self.transport.send(
            payload
        )


    async def _on_message(
        self,
        payload: Any,
    ) -> None:

        packet = self.parser.decode(
            payload
        )


        if isinstance(packet, Response):

            if self.client:

                self.client.handle_response(
                    packet
                )

            return


        if self.server:

            await self.server.receive(
                packet
            )


    async def close(self) -> None:

        await self.transport.close()
