from datetime import datetime

from fastapi import Request
from starlette_context import context


async def middleware(request: Request, call_next):
    time = datetime.now()
    context['time'] = time
    return await call_next(request)
