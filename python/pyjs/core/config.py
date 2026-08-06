from dataclasses import dataclass

from .constants import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
    DEFAULT_SERIALIZER,
    DEFAULT_TRANSPORT,
    DEFAULT_LOG_LEVEL,
)


@dataclass(slots=True)
class Config:
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT

    timeout: int = DEFAULT_TIMEOUT

    serializer: str = DEFAULT_SERIALIZER

    transport: str = DEFAULT_TRANSPORT

    debug: bool = False

    log_level: str = DEFAULT_LOG_LEVEL
