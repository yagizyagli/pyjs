"""
protocol.factory

Packet object creation from raw payloads.
"""

from __future__ import annotations

from typing import Any

from .packet import Packet
from .request import Request
from .response import Response
from .event import Event

from .enums import PacketType
from .exceptions import InvalidPacketTypeError


class PacketFactory:
    """
    Creates packet instances from dictionaries.
    """


    _types = {
        PacketType.REQUEST.value: Request,
        PacketType.RESPONSE.value: Response,
        PacketType.EVENT.value: Event,
    }


    @classmethod
    def register(
        cls,
        packet_type: str,
        packet_class: type[Packet],
    ) -> None:

        cls._types[packet_type] = packet_class


    @classmethod
    def create(
        cls,
        payload: dict[str, Any],
    ) -> Packet:


        packet_type = payload.get(
            "type"
        )


        if packet_type is None:

            raise InvalidPacketTypeError(
                "Packet type missing."
            )


        packet_class = cls._types.get(
            packet_type
        )


        if packet_class is None:

            raise InvalidPacketTypeError(
                f"Unsupported packet type: {packet_type}"
            )


        return packet_class.from_dict(
            payload
        )


    @classmethod
    def types(cls) -> tuple[str, ...]:

        return tuple(
            cls._types.keys()
        )
