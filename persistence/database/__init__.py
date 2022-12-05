"""
Controls the connection / driver of database.
------

分類的邏輯：拿出來的東西是什麼，就放在哪個檔案
"""


import asyncpg

from base import mcs
from config import DBConfig


class PoolHandler(metaclass=mcs.Singleton):
    def __init__(self):
        self._pool: asyncpg.pool.Pool = None  # Need to be init/closed manually

    async def initialize(self, db_config: DBConfig):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                host=db_config.host,
                port=db_config.port,
                user=db_config.username,
                password=db_config.password,
                database=db_config.db_name,
                max_size=db_config.max_pool_size,
            )

    async def close(self):
        if self._pool is not None:
            await self._pool.close()

    @property
    def pool(self):
        return self._pool


pool_handler = PoolHandler()


# For import usage
from . import (
    account,
    s3_file,
)
