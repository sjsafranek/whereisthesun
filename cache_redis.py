import json
import redis
from redis.maint_notifications import MaintNotificationsConfig

from conf import REDIS_HOST
from conf import REDIS_PORT


def isEnabled():
    return None != REDIS_HOST


# Connect to a local Redis instance
r = redis.Redis(
	host=REDIS_HOST, 
	port=REDIS_PORT, 
	db=0, 
	decode_responses=True,
	maint_notifications_config=MaintNotificationsConfig(enabled=False)
)

def set(key, value, ttl_seconds=3600):
	r.setex(f'sun:{key}', ttl_seconds, json.dumps(value))  # Expires in 1 hour

def _set(key, value, ttl_seconds=3600):
	r.setex(f'sun:{key}', ttl_seconds, value)  # Expires in 1 hour

def get(key):
	item = r.get(f'sun:{key}')
	if not item:
		return None
	return json.loads(item) 
