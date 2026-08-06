class ProtocolError(Exception):
    pass


class InvalidPacketError(ProtocolError):
    pass


class InvalidVersionError(ProtocolError):
    pass


class InvalidPacketTypeError(ProtocolError):
    pass


class ValidationError(ProtocolError):
    pass


class CodecError(ProtocolError):
    pass
