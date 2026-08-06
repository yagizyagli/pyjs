"""
PyJS

Python <-> JavaScript bridge framework.
"""

from .bridge import (
    Bridge,
    Client,
    Server,
    Router,
    Dispatcher,
    Middleware,
    MiddlewarePipeline,
)

from .protocol import (
    Packet,
    Request,
    Response,
    Event,

    PacketType,
    PacketPriority,
    PacketStatus,

    Protocol,

    Codec,
    JSONCodec,
    CodecRegistry,

    PROTOCOL_NAME,
    PROTOCOL_VERSION,
)


__version__ = "1.0.0"


__all__ = [

    # Core
    "Bridge",
    "Client",
    "Server",
    "Router",
    "Dispatcher",


    # Middleware
    "Middleware",
    "MiddlewarePipeline",


    # Protocol models
    "Packet",
    "Request",
    "Response",
    "Event",


    # Protocol
    "Protocol",
    "PacketType",
    "PacketPriority",
    "PacketStatus",


    # Codec
    "Codec",
    "JSONCodec",
    "CodecRegistry",


    # Version
    "PROTOCOL_NAME",
    "PROTOCOL_VERSION",
]
