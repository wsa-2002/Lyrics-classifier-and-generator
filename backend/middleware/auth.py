from datetime import datetime

from fastapi import Request
from starlette_context import context

import security


async def middleware(request: Request, call_next):
    time = datetime.now()
    account = None
    if auth_token := request.headers.get('auth-token', None):
        account = security.decode_jwt(auth_token, time=time)
    context['account'] = account
    context['time'] = time
    return await call_next(request)
