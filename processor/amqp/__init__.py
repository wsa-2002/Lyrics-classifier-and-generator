import json
import dataclasses

import pydantic

from base import do
import persistence.database as db

# template for unmarshal mq message
# def unmarshal_report(body: bytes) -> do.JudgeReport:
#     return pydantic.parse_raw_as(do.JudgeReport, body.decode())


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def marshal(obj) -> bytes:
    return json.dumps(obj, cls=EnhancedJSONEncoder).encode()
