from __future__ import annotations

import asyncio
from time import monotonic

from .models import PendingRequest


class FutureManager:

    def __init__(self) -> None:

        self._pending: dict[str, PendingRequest] = {}

    def create(
        self,
        request_id: str,
        method: str,
        timeout: float,
        metadata: dict | None = None,
    ) -> PendingRequest:

        future = asyncio.get_running_loop().create_future()

        request = PendingRequest(
            id=request_id,
            method=method,
            future=future,
            timeout=timeout,
            metadata=metadata or {},
        )

        self._pending[request_id] = request

        return request

    def resolve(
        self,
        request_id: str,
        value,
    ) -> None:

        req = self._pending.pop(request_id)

        req.completed = True

        if not req.future.done():
            req.future.set_result(value)

    def reject(
        self,
        request_id: str,
        exc,
    ) -> None:

        req = self._pending.pop(request_id)

        req.completed = True

        if not req.future.done():
            req.future.set_exception(exc)

    def cancel(
        self,
        request_id: str,
    ) -> None:

        req = self._pending.pop(request_id)

        req.cancelled = True

        if not req.future.done():
            req.future.cancel()

    def expire(self) -> None:

        now = monotonic()

        expired: list[str] = []

        for request_id, req in self._pending.items():

            if now - req.created_at >= req.timeout:

                expired.append(request_id)

        for request_id in expired:

            self.cancel(request_id)

    def pending(self) -> tuple[PendingRequest, ...]:

        return tuple(self._pending.values())

    def clear(self) -> None:

        for req in self._pending.values():

            if not req.future.done():
                req.future.cancel()

        self._pending.clear()
