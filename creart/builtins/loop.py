from __future__ import annotations

import asyncio
from asyncio import AbstractEventLoop

from .. import AbstractCreator, CreateTargetInfo


class EventLoopCreator(AbstractCreator):
    targets = (CreateTargetInfo("asyncio.events", "AbstractEventLoop"),)

    @staticmethod
    def create(_: type[AbstractEventLoop]) -> AbstractEventLoop:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop
