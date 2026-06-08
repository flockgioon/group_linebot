from typing import Callable

_listeners: list[Callable[[str], list]] = []


def listener(fn: Callable[[str], list]):
    _listeners.append(fn)
    return fn


def check_all(text: str) -> list:
    messages = []
    for fn in _listeners:
        result = fn(text)
        if result:
            messages.extend(result)
    return messages


import listeners.mygo
