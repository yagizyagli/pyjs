"""
Public codec API.
"""

from .base import Codec
from .json import JSONCodec
from .registry import CodecRegistry

from .exceptions import (
    CodecError,
    EncodeError,
    DecodeError,
    UnsupportedCodecError,
)


__all__ = [
    "Codec",
    "JSONCodec",
    "CodecRegistry",
    "CodecError",
    "EncodeError",
    "DecodeError",
    "UnsupportedCodecError",
]
