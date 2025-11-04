from redis import Redis
from rq import Queue
from rq.job import Job

queue=Queue(connection=Redis(
    host="localhost",
    port=6379,
))