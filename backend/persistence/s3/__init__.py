import aioboto3
import typing
from uuid import UUID

from base import mcs
from config import S3Config


class S3Handler(metaclass=mcs.Singleton):
    def __init__(self):
        self._session = aioboto3.Session()
        self._client = None
        self._resource = None

    async def initialize(self, s3_config: S3Config):
        self._client = await self._session.client(
            's3',
            endpoint_url=s3_config.endpoint,
            aws_access_key_id=s3_config.access_key,
            aws_secret_access_key=s3_config.secret_key,
        ).__aenter__()

        self._resource = await self._session.resource(
            's3',
            endpoint_url=s3_config.endpoint,
            aws_access_key_id=s3_config.access_key,
            aws_secret_access_key=s3_config.secret_key,
        ).__aenter__()

    async def close(self):
        await self._client.close()
        await self._resource.close()

    async def sign_url(self, bucket: str, key: str, filename: str) -> str:
        return await self._client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket,
                'Key': key,
                'ResponseContentDisposition': f"attachment; filename={filename};"
            },
            ExpiresIn=3600,
        )

    async def upload(self, file: typing.IO, key: UUID, bucket_name: str = 'temp'):
        bucket = await self._resource.Bucket(bucket_name)
        await bucket.upload_fileobj(file, str(key))


s3_handler = S3Handler()
