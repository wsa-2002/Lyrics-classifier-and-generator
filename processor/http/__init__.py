import fastapi


def register_routers(app: fastapi.FastAPI):
    from . import (
        account,
        public,
    )

    app.include_router(public.router)
    app.include_router(account.router)
