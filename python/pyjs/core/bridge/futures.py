from __future__ import annotations

import asyncio
import uuid
from time import monotonic

from .models import PendingRequest


class FutureManager:

    def __init__(self):

        self._pending: dict[str, PendingRequest] = {}

    def create(
        self,
        method: str,
        timeout: float,
        metadata: dict | None = None,
    ) -> PendingRequest:

        rid = uuid.uuid4().hex

        future = asyncio.get_running_loop().create_future()

        request = PendingRequest(
            id=rid,
            method=method,
            future=future,
            timeout=timeout,
            metadata=metadata or {},
        )

        self._pending[rid] = request

        return request

    def resolve(self, rid: str, value):

        req = self._pending.pop(rid)

        req.completed = True

        if not req.future.done():
            req.future.set_result(value)

    def reject(self, rid: str, exc):

        req = self._pending.pop(rid)

        req.completed = True

        if not req.future.done():
            req.future.set_exception(exc)

    def cancel(self, rid: str):

        req = self._pending.pop(rid)

        req.cancelled = True

        if not req.future.done():
            req.future.cancel()

    def expire(self):

        now = monotonic()

        expired = []

        for rid, req in self._pending.items():

            if now - req.created_at >= req.timeout:

                expired.append(rid)

        for rid in expired:

            self.cancel(rid)

    def pending(self):

        return tuple(self._pending.values())

    def clear(self):

        for req in self._pending.values():

            if not req.future.done():
                req.future.cancel()

        self._pending.clear()
