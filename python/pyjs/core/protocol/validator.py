"""
protocol/validator.py
"""

from __future__ import annotations

from .exceptions import ValidationError
from .packet import Packet


class PacketValidator:

    def validate(self, packet: Packet) -> None:

        if not packet.id:
            raise ValidationError("Packet id is required.")

        if not packet.protocol:
            raise ValidationError("Protocol name is required.")

        if not packet.version:
            raise ValidationError("Protocol version is required.")

        if not packet.magic:
            raise ValidationError("Protocol magic is required.")

        if packet.timestamp <= 0:
            raise ValidationError("Invalid timestamp.")
