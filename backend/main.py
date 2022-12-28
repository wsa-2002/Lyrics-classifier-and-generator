import random
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import app_config

app = FastAPI(
    title=app_config.title,
    docs_url=app_config.docs_url,
    redoc_url=app_config.redoc_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def app_startup():
    random.seed(time.time())


import middleware.auth  # noqa E402

app.middleware('http')(middleware.auth.middleware)

import starlette_context.middleware  # noqa E402

app.add_middleware(starlette_context.middleware.RawContextMiddleware)

import processor.http  # noqa E402

processor.http.register_routers(app)
