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
    from config import db_config
    from persistence.database import pool_handler
    await pool_handler.initialize(db_config=db_config)

    # if s3 needed
    from config import s3_config
    from persistence.s3 import s3_handler
    await s3_handler.initialize(s3_config=s3_config)

    # if amqp needed
    from config import amqp_config
    from persistence.amqp_publisher import amqp_publish_handler
    await amqp_publish_handler.initialize(amqp_config=amqp_config)

    from persistence.amqp_consumer import make_consumer
    import processor.amqp
    report_consumer = make_consumer(amqp_config=amqp_config,
                                    consume_function=processor.amqp.save_report)

    import asyncio
    asyncio.ensure_future(report_consumer(asyncio.get_event_loop()))


@app.on_event('shutdown')
async def app_shutdown():
    from persistence.database import pool_handler
    await pool_handler.close()

    # if s3 needed
    from persistence.s3 import s3_handler
    await s3_handler.close()

    # if amqp needed
    from persistence.amqp_publisher import amqp_publish_handler
    await amqp_publish_handler.close()


import middleware.auth
app.middleware('http')(middleware.auth.middleware)

import starlette_context.middleware
app.add_middleware(starlette_context.middleware.RawContextMiddleware)

import processor.http
processor.http.register_routers(app)
