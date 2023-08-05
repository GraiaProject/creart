from __future__ import annotations

import asyncio
from asyncio import AbstractEventLoop
from contextlib import suppress

from .. import AbstractCreator, CreateTargetInfo


class EventLoopCreator(AbstractCreator):
    targets = (CreateTargetInfo("asyncio.events", "AbstractEventLoop"),)

    @staticmethod
    def create(_: type[AbstractEventLoop]) -> AbstractEventLoop:
        with suppress(Exception):
            # This will become an error if there is no running event loop
            # and no current loop is set in some future Python release.
            # But we don't know what exception will be raised,
            # so we just suppress all exceptions now.
            loop = asyncio.get_event_loop()
            if not loop.is_closed():
                return loop

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop
