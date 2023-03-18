from typing import Callable

# List with registered event callbacks
__registered_callbacks = {}


# Registers a callback that listens for a given signal
def start_lurking(signal: str, callback: Callable[[any], any]) -> object:
    if signal not in __registered_callbacks:
        __registered_callbacks[signal] = []

    __registered_callbacks[signal].append(callback)


# Sends an event with any data that is given
def shout(signal: str, data: any = None):
    if signal not in __registered_callbacks:
        return

    for cb in __registered_callbacks[signal]:
        cb(data)


# Removes a callback
def stop_lurking(signal: str, callback: Callable[[any], any]):
    if signal not in __registered_callbacks:
        return

    __registered_callbacks[signal].remove(callback)
