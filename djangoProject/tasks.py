

# app/tasks.py, 可以复用的task
from celery import shared_task, Celery
import time

app = Celery('djangoProject')

@app.task
def hello():
    return "hello"

@shared_task
def add(x, y):
    time.sleep(2)
    return x + y