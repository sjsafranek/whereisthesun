import time
import functools
import logging

import cache_redis
import cache_memory


logging.info(f'Redis enabled ${cache_redis.isEnabled()}')


def set(key, value, ttl_seconds=3600):
    if cache_redis.isEnabled():
        cache_redis.set(key, value, ttl_seconds=ttl_seconds)
        return
    cache_memory.set(key, value, ttl_seconds=ttl_seconds)


def get(key):
    if cache_redis.isEnabled():
        return cache_redis.get(key)
    return cache_memory.get(key)


def time_cache(max_age, maxsize=128, typed=False):
    """Least-recently-used cache decorator with time-based cache invalidation.

    Args:
        max_age: Time to live for cached results (in seconds).
        maxsize: Maximum cache size (see `functools.lru_cache`).
        typed: Cache on distinct input types (see `functools.lru_cache`).
    """
    def _decorator(fn):
        @functools.lru_cache(maxsize=maxsize, typed=typed)
        def _new(*args, __time_salt, **kwargs):
            return fn(*args, **kwargs)

        @functools.wraps(fn)
        def _wrapped(*args, **kwargs):
            return _new(*args, **kwargs, __time_salt=int(time.time() / max_age))

        return _wrapped

    return _decorator
