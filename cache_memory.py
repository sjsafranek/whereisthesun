import time
from functools import wraps


MEMORY = {}


def _clean():
    now = time.monotonic()
    keys = MEMORY.keys()
    for key in keys:
        value, expiration = MEMORY[key]
        if now > expiration:
            print(f'del {key}')
            del MEMORY[key]


def set(key, value, ttl_seconds=3600):
    _clean()
    now = time.monotonic()
    MEMORY[key] =  (value, now + ttl_seconds)


def get(key):
    _clean()
    now = time.monotonic()
    if key in MEMORY:
        return MEMORY[key][0]
