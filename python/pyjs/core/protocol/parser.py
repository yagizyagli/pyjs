"""
protocol.parser

Raw payload parser.
"""

from __future__ import annotations

from typing import Any

from .codec import Codec
from .packet import Packet
from .factory import PacketFactory


class PacketParser:
    """
    Converts raw encoded data into Packet objects.
    """


    def __init__(
        self,
        codec: Codec,
    ) -> None:

        self.codec = codec


    def encode(
        self,
        packet: Packet,
    ) -> bytes | str:

        payload = packet.to_dict()

        return self.codec.encode(
            payload
        )


    def decode(
        self,
        payload: bytes | str,
    ) -> Packet:

        data: dict[str, Any] = (
            self.codec.decode(payload)
        )

        return PacketFactory.create(
            data
        )
