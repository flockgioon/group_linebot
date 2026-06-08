import re
from typing import Callable

_keyword_to_handler: dict[str, Callable[[str], list]] = {}


def command(*keywords: str):
    def decorator(fn: Callable[[str], list]):
        for kw in keywords:
            _keyword_to_handler[kw] = fn
        return fn
    return decorator


def dispatch(text: str) -> list | None:
    parts = re.split(r"[ \n]", text, maxsplit=1)
    keyword = parts[0]
    rest = parts[1] if len(parts) > 1 else ""

    handler = _keyword_to_handler.get(keyword)
    if handler is None:
        return None
    return handler(rest)


import commands.readme
import commands.dice
import commands.coin
import commands.weather
import commands.stock
import commands.satellite
