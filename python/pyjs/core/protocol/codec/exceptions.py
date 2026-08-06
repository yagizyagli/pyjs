"""
Codec exceptions.
"""


class CodecError(Exception):
    """
    Base codec exception.
    """


class UnsupportedCodecError(CodecError):
    """
    Codec is not registered.
    """


class EncodeError(CodecError):
    """
    Serialization failed.
    """


class DecodeError(CodecError):
    """
    Deserialization failed.
    """
