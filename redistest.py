import redis

redis_conn = redis.Redis(host="127.0.0.1", port=6379)
redis_conn.psetex("test",30000,"1")