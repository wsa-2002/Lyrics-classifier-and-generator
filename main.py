from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import app_config

app = FastAPI(
    title=app_config.title,
    docs_url=app_config.docs_url,
    redoc_url=app_config.redoc_url,
)

origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://localhost:3006',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def app_startup():
    pass


@app.on_event('shutdown')
async def app_shutdown():
    pass


import middleware.auth

app.middleware('http')(middleware.auth.middleware)

import starlette_context.middleware

app.add_middleware(starlette_context.middleware.RawContextMiddleware)

import processor.http

processor.http.register_routers(app)
