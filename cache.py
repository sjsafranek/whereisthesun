import logging

import redis
from redis.maint_notifications import MaintNotificationsConfig

import cache_redis
import cache_memory


logger = logging.getLogger(__name__)
logger.info(f'Redis enabled ${cache_redis.isEnabled()}')


def set(key, value, ttl_seconds=3600):
    if cache_redis.isEnabled():
        cache_redis.set(key, value, ttl_seconds=ttl_seconds)
    cache_memory.set(key, value, ttl_seconds=ttl_seconds)


def get(key):
    if cache_redis.isEnabled():
        return cache_redis.get(key)
    return cache_memory.get(key)

