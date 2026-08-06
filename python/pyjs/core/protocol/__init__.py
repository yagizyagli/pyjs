"""
Protocol public API.
"""

from .version import (
    PROTOCOL_NAME,
    PROTOCOL_VERSION,
    SUPPORTED_VERSIONS,
)

from .enums import (
    PacketType,
    PacketPriority,
    PacketStatus,
)

from .exceptions import (
    ProtocolError,
    InvalidPacketError,
    InvalidVersionError,
    InvalidPacketTypeError,
    ValidationError,
    CodecError,
)

from .packet import Packet

from .request import Request

from .response import Response

from .event import Event

from .validator import PacketValidator

from .protocol import Protocol


from .codec import (
    Codec,
    JSONCodec,
    CodecRegistry,
)


__all__ = [

    # Version
    "PROTOCOL_NAME",
    "PROTOCOL_VERSION",
    "SUPPORTED_VERSIONS",


    # Enums
    "PacketType",
    "PacketPriority",
    "PacketStatus",


    # Exceptions
    "ProtocolError",
    "InvalidPacketError",
    "InvalidVersionError",
    "InvalidPacketTypeError",
    "ValidationError",
    "CodecError",


    # Models
    "Packet",
    "Request",
    "Response",
    "Event",


    # Validation
    "PacketValidator",


    # Protocol
    "Protocol",


    # Codec
    "Codec",
    "JSONCodec",
    "CodecRegistry",
]
