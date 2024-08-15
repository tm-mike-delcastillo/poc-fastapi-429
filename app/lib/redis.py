import json
import math
import os
import time
import redis


def get():
    return "Hello World"

def redis_client():
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    REDIS_PORT = os.getenv('REDIS_PORT')
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)

RATE_LIMIT_MESSAGES_COUNT = 5
RATE_LIMIT_MESSAGES_DURATION = 5 * 60 * 1000

def should_rate_limit_message(user_id: str) -> bool:
    key = f"message_limit:{user_id}"
    now = math.floor(time.time() * 1000)
    try:

        redis = redis_client()
        raw_data = redis.get(key)
        timestamps = json.loads(raw_data) if raw_data else []
        
        recent_timestamps = [timestamp for timestamp in timestamps if timestamp > now - RATE_LIMIT_MESSAGES_DURATION]
        should_rate_limit = len(recent_timestamps) >= RATE_LIMIT_MESSAGES_COUNT

        if not should_rate_limit:
            recent_timestamps.append(now)
            redis.set(key, json.dumps(recent_timestamps))
            
        return should_rate_limit
    except Exception as e:
        raise e
        # log properly
    return False
    