import redis

messeger = redis.Redis(
    host='localhost',
     port=6379,
     db=0
)
