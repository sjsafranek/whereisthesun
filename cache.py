import json
import redis
from redis.maint_notifications import MaintNotificationsConfig

# Connect to a local Redis instance
r = redis.Redis(
	host='localhost', 
	port=6379, 
	db=0, 
	decode_responses=True,
	maint_notifications_config=MaintNotificationsConfig(enabled=False)
)

def set(key, value, expires=3600):
	r.setex(f'sun:{key}', expires, json.dumps(value))  # Expires in 1 hour

def _set(key, value, expires=3600):
	r.setex(f'sun:{key}', expires, value)  # Expires in 1 hour


def get(key):
	item = r.get(f'sun:{key}')
	if not item:
		return None
	return json.loads(item) 
