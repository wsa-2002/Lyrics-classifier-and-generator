from functools import wraps


# decorator
def enveloped(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            data = await func(*args, **kwargs)
        except Exception as e:
            print(e)
            return {
                'data': None,
                'error': e.__class__.__name__,
            }
        else:
            return {
                'data': data,
                'error': None
            }
    return wrapped
