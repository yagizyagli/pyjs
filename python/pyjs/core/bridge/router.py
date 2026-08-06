"""
bridge.router

RPC and event routing system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


Handler = Callable[..., Any]


@dataclass(slots=True)
class Route:

    name: str

    handler: Handler

    namespace: str = "default"

    metadata: dict[str, Any] | None = None

    @property
    def full_name(self) -> str:
        return f"{self.namespace}.{self.name}"


class Router:

    def __init__(self) -> None:

        self._routes: dict[str, Route] = {}

        self._events: dict[str, list[Handler]] = {}


    def register(
        self,
        name: str,
        handler: Handler,
        namespace: str = "default",
        metadata: dict[str, Any] | None = None,
    ) -> Route:

        route = Route(
            name=name,
            handler=handler,
            namespace=namespace,
            metadata=metadata,
        )

        self._routes[route.full_name] = route

        return route


    def unregister(
        self,
        name: str,
        namespace: str = "default",
    ) -> None:

        key = f"{namespace}.{name}"

        self._routes.pop(key, None)


    def resolve(
        self,
        name: str,
        namespace: str = "default",
    ) -> Route | None:

        key = f"{namespace}.{name}"

        return self._routes.get(key)


    def has(
        self,
        name: str,
        namespace: str = "default",
    ) -> bool:

        return self.resolve(name, namespace) is not None


    def methods(self) -> tuple[str, ...]:

        return tuple(self._routes.keys())


    def on(
        self,
        event: str,
        handler: Handler,
    ) -> None:

        listeners = self._events.setdefault(
            event,
            [],
        )

        listeners.append(handler)


    def off(
        self,
        event: str,
        handler: Handler,
    ) -> None:

        listeners = self._events.get(event)

        if not listeners:
            return

        if handler in listeners:
            listeners.remove(handler)


    def listeners(
        self,
        event: str,
    ) -> tuple[Handler, ...]:

        return tuple(
            self._events.get(event, [])
        )


    def clear(self) -> None:

        self._routes.clear()

        self._events.clear()
