import fastapi


def register_routers(app: fastapi.FastAPI):
    from . import (
        public,
    )

    app.include_router(public.router)
