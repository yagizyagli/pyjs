"""
bridge.middleware

Middleware pipeline system.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable


NextHandler = Callable[[Any], Awaitable[Any]]


class Middleware(ABC):
    """
    Base middleware interface.
    """

    @abstractmethod
    async def handle(
        self,
        context: Any,
        next: NextHandler,
    ) -> Any:
        raise NotImplementedError



class MiddlewarePipeline:

    def __init__(self) -> None:

        self._middlewares: list[Middleware] = []


    def add(
        self,
        middleware: Middleware,
    ) -> None:

        self._middlewares.append(
            middleware
        )


    def remove(
        self,
        middleware: Middleware,
    ) -> None:

        if middleware in self._middlewares:

            self._middlewares.remove(
                middleware
            )


    async def execute(
        self,
        context: Any,
        final: NextHandler,
    ) -> Any:


        async def dispatch(
            index: int,
            ctx: Any,
        ) -> Any:

            if index >= len(self._middlewares):

                return await final(ctx)


            middleware = self._middlewares[index]


            return await middleware.handle(
                ctx,
                lambda new_ctx: dispatch(
                    index + 1,
                    new_ctx,
                ),
            )


        return await dispatch(
            0,
            context,
        )


    def clear(self) -> None:

        self._middlewares.clear()


    def count(self) -> int:

        return len(
            self._middlewares
        )
