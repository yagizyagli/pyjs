"""
Core runtime engine.
"""

from __future__ import annotations

from .constants import (
    ENGINE_RUNNING,
    ENGINE_STARTING,
    ENGINE_STOPPED,
    ENGINE_STOPPING,
)


class Engine:
    def __init__(self):
        self._state = ENGINE_STOPPED

    @property
    def state(self):
        return self._state

    @property
    def running(self):
        return self._state == ENGINE_RUNNING

    def start(self):
        if self.running:
            return

        self._state = ENGINE_STARTING

        # Runtime initialization will be added later.

        self._state = ENGINE_RUNNING

    def stop(self):
        if not self.running:
            return

        self._state = ENGINE_STOPPING

        # Runtime shutdown will be added later.

        self._state = ENGINE_STOPPED

    def restart(self):
        self.stop()
        self.start()
