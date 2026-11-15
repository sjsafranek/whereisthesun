
import time
from functools import wraps

def ttl_cache(ttl_seconds):
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a hashable key from arguments
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()

            if key in cache:
                result, expiration = cache[key]
                if now < expiration:
                    return result

            # Compute and store new value
            result = func(*args, **kwargs)
            cache[key] = (result, now + ttl_seconds)
            return result

        return wrapper
    return decorator
