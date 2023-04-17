import redis

messeger = redis.Redis(
    host='messeger',
    port=6379,
    db=0
)
