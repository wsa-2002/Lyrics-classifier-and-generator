from fastapi import Header


async def get_auth_token(auth_token: str = Header(None, convert_underscores=True)):
    pass
