import requests
from celery import Celery
from celery.utils.log import get_task_logger


app = Celery(
    'tasks', 
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

logger = get_task_logger(__name__)


@app.task(
    autoretry_for=(Exception,),
    default_retry_delay=10,
    retry_kwargs={'max_retries': 5}
)
def create_task():
    response = requests.get("http://localhost:5000")
    json_data = response.json()
    return json_data["_links"]["task"]

@app.task(
    bind=True,
    default_retry_delay=10,
    retry_kwargs={'max_retries': 5}
)
def get_task_info(self, link_url):
    response = requests.get(link_url)
    json_data = response.json()
    if json_data["state"] != "SUCCESS":
        raise self.retry()
    return json_data


@app.task
def add(x, y):
    return x + y


@app.task
def mul_list(args):
    result = 1
    logger.info(f"result initial {result}")
    for i in args:
        logger.info(f"result {result} * {i}")
        result *= i
    return result

