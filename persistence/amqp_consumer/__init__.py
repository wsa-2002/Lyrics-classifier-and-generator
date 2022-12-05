import asyncio
from typing import Callable, Coroutine, Any

import aio_pika

from config import AMQPConfig, AMQP_CONSUME_QUEUE


def make_consumer(amqp_config: AMQPConfig, consume_function: Callable[[bytes], Coroutine[Any, Any, None]]) \
        -> Callable[[asyncio.events.AbstractEventLoop], Coroutine[Any, Any, None]]:
    async def main(loop: asyncio.events.AbstractEventLoop):
        async with await aio_pika.connect(
                host=amqp_config.host,
                port=amqp_config.port,
                login=amqp_config.username,
                password=amqp_config.password,
                loop=loop,
        ) as connection:
            channel: aio_pika.RobustChannel = await connection.channel()
            queue = await channel.declare_queue(
                AMQP_CONSUME_QUEUE,
                durable=True,
            )

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    message: aio_pika.IncomingMessage
                    try:
                        await consume_function(message.body)
                    except Exception as e:
                        print(e)
                        await message.nack(requeue=False)
                    else:
                        await message.ack()

    return main

