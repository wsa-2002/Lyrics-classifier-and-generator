import aio_pika

from config import AMQPConfig, AMQP_PUBLISH_QUEUE
from base import mcs, do
from processor.amqp import marshal


class AMQPPublishHandler(metaclass=mcs.Singleton):
    def __init__(self):
        self._connection: aio_pika.Connection = None  # Need to be init/closed manually
        self._channel: aio_pika.Channel = None  # Need to be init/closed manually

    async def initialize(self, amqp_config: AMQPConfig):
        self._connection = await aio_pika.connect(
            host=amqp_config.host,
            port=amqp_config.port,
            login=amqp_config.username,
            password=amqp_config.password,
        )
        self._channel = await self._connection.channel().__aenter__()

    async def close(self):
        await self._channel.close()
        await self._connection.close()

    async def publish(self, queue_name: str, message: bytes):
        await self._channel.default_exchange.publish(aio_pika.Message(body=message), routing_key=queue_name)


amqp_publish_handler = AMQPPublishHandler()
