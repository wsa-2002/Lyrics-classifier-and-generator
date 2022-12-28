from datetime import datetime

from starlette_context import context

from base import mcs


class Request(metaclass=mcs.Singleton):
    _context = context

    @property
    def time(self) -> datetime:
        return self._context.get('time')


request = Request()
