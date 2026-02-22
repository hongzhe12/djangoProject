import time
from celery import shared_task


@shared_task(bind=True)
def add_numbers(self, a: int, b: int):
    time.sleep(1)
    return a + b


@shared_task(bind=True)
def slow_echo(self, message: str, delay: int = 3):
    time.sleep(max(delay, 0))
    return message
