"""
bridge.dispatcher

Packet dispatching engine.
"""

from __future__ import annotations

import inspect
from typing import Any

from protocol.event import Event
from protocol.packet import Packet
from protocol.request import Request
from protocol.response import Response

from .router import Router


class Dispatcher:

    def __init__(
        self,
        router: Router,
    ) -> None:

        self.router = router


    async def dispatch(
        self,
        packet: Packet,
    ) -> Response | None:

        if isinstance(packet, Request):

            return await self._dispatch_request(packet)


        if isinstance(packet, Event):

            await self._dispatch_event(packet)

            return None


        return None


    async def _dispatch_request(
        self,
        request: Request,
    ) -> Response:

        route = self.router.resolve(
            request.method
        )


        if route is None:

            return Response(
                request_id=request.id,
                success=False,
                error={
                    "code": "METHOD_NOT_FOUND",
                    "message": (
                        f"Method not found: "
                        f"{request.method}"
                    ),
                },
            )


        try:

            result = route.handler(
                *request.args,
                **request.kwargs,
            )


            if inspect.isawaitable(result):

                result = await result


            return Response(
                request_id=request.id,
                success=True,
                result=result,
            )


        except Exception as exc:

            return Response(
                request_id=request.id,
                success=False,
                error={
                    "code": type(exc).__name__,
                    "message": str(exc),
                },
            )


    async def _dispatch_event(
        self,
        event: Event,
    ) -> None:

        listeners = self.router.listeners(
            event.name
        )


        for listener in listeners:

            result = listener(
                event.data
            )

            if inspect.isawaitable(result):

                await result
