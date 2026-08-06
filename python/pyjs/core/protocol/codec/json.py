"""
protocol.codec.json

JSON serializer implementation.
"""

from __future__ import annotations

import json
from typing import Any

from .base import Codec
from .exceptions import DecodeError, EncodeError


class JSONCodec(Codec):
    """
    JSON based codec.
    """

    name = "json"

    content_type = "application/json"

    binary = False

    def encode(self, data: Any) -> str:
        try:
            return json.dumps(
                data,
                ensure_ascii=False,
                separators=(",", ":"),
            )

        except Exception as exc:
            raise EncodeError(
                f"JSON encode failed: {exc}"
            ) from exc

    def decode(self, payload: str | bytes) -> Any:
        try:
            if isinstance(payload, bytes):
                payload = payload.decode("utf-8")

            return json.loads(payload)

        except Exception as exc:
            raise DecodeError(
                f"JSON decode failed: {exc}"
            ) from exc
