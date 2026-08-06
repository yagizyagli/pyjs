"""
Pending request manager.
"""

from __future__ import annotations

import asyncio
import uuid
from typing import Any


class FutureManager:
    """
    Stores pending RPC requests.
    """

    def __init__(self) -> None:
        self._futures: dict[str, asyncio.Future[Any]] = {}

    def create(self) -> tuple[str, asyncio.Future[Any]]:
        request_id = str(uuid.uuid4())

        future = asyncio.get_running_loop().create_future()

        self._futures[request_id] = future

        return request_id, future

    def resolve(self, request_id: str, result: Any) -> bool:
        future = self._futures.pop(request_id, None)

        if future is None:
            return False

        if not future.done():
            future.set_result(result)

        return True

    def reject(self, request_id: str, error: Exception) -> bool:
        future = self._futures.pop(request_id, None)

        if future is None:
            return False

        if not future.done():
            future.set_exception(error)

        return True

    def cancel(self, request_id: str) -> bool:
        future = self._futures.pop(request_id, None)

        if future is None:
            return False

        future.cancel()

        return True

    def exists(self, request_id: str) -> bool:
        return request_id in self._futures

    def get(self, request_id: str) -> asyncio.Future[Any]:
        return self._futures[request_id]

    def pending(self) -> int:
        return len(self._futures)

    def clear(self) -> None:
        for future in self._futures.values():
            if not future.done():
                future.cancel()

        self._futures.clear()
