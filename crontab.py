# coding:utf-8
import docker
import redis

# 删除超时的容器
client = docker.from_env(version="auto")

redis_conn = redis.Redis(host="127.0.0.1", port=6379)
containers = []
for key in redis_conn.keys():
    try:
        containers.insert(0, redis_conn.get(key))
    except Exception as e:
        print e
for i in client.containers.list():
    if "vuln/" in str(i.image):
        if i.id not in containers:
            try:
                client.api.stop(i.id)
                client.api.remove_container(i.id)
            except Exception as e:
                print e
