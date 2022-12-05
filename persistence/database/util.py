import collections
import itertools
from typing import Any, Tuple, List


# modify from https://github.com/MagicStack/asyncpg/issues/9#issuecomment-600659015
def pyformat2psql(sql: str, parameters: dict[str, any] = None, **params) -> Tuple[str, List[Any]]:
    named_args = {**params}
    if parameters:
        named_args.update(parameters)
    positional_generator = itertools.count(1)
    positional_map = collections.defaultdict(lambda: '${}'.format(next(positional_generator)))
    formatted_query = sql % positional_map
    positional_items = sorted(
        positional_map.items(),
        key=lambda item: int(item[1].replace('$', '')),
    )
    positional_args = [named_args[named_arg] for named_arg, _ in positional_items]
    print(formatted_query, positional_args)
    return formatted_query, positional_args
