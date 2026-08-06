"""
protocol/protocol.py
"""

from __future__ import annotations

from .validator import PacketValidator


class Protocol:

    def __init__(self):

        self.validator = PacketValidator()

    def encode(self, packet, codec):

        self.validator.validate(packet)

        return codec.encode(packet)

    def decode(self, payload, codec):

        packet = codec.decode(payload)

        self.validator.validate(packet)

        return packet
