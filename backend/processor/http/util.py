from datetime import datetime

import pydantic


def timezone_validate(time: datetime) -> datetime:
    converted = pydantic.datetime_parse.parse_datetime(time)

    if converted.tzinfo is not None:
        # Convert to server time
        converted = converted.astimezone().replace(tzinfo=None)

    return converted
