import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)


def setDeclined(task_id, task_title):
    r.hset('task', task_id, task_title)


def getDeclined():
    return r.hgetall('task')


def delDeclined():
    keys = getDeclined().keys()
    return r.hdel('task', *keys)


