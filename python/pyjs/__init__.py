"""
PyJS

Python <-> JavaScript bridge framework.
"""

from .core.bridge import (
    Bridge,
    Client,
    Server,
    Router,
    Dispatcher,
    Middleware,
    MiddlewarePipeline,
)

from .core.protocol import (
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
    "Bridge",
    "Client",
    "Server",
    "Router",
    "Dispatcher",
    "Middleware",
    "MiddlewarePipeline",
    "Packet",
    "Request",
    "Response",
    "Event",
    "Protocol",
    "PacketType",
    "PacketPriority",
    "PacketStatus",
    "Codec",
    "JSONCodec",
    "CodecRegistry",
    "PROTOCOL_NAME",
    "PROTOCOL_VERSION",
]
