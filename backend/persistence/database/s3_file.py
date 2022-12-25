from base import do

from .util import pyformat2psql
from . import pool_handler


async def add(s3_file: do.S3File) -> None:
    sql, params = pyformat2psql(
        sql=fr"INSERT INTO s3_file"
            fr"            (uuid, key, bucket)"
            fr"     VALUES (%(uuid)s, %(key)s, %(bucket)s)",
        uuid=s3_file.uuid, key=s3_file.key, bucket=s3_file.bucket,
    )
    await pool_handler.pool.execute(sql, *params)
