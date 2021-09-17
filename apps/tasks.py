import random
import time

from celery.utils.log import get_task_logger

from apps.extensions import celery


logger = get_task_logger(__name__)

@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ["Starting up", "Booting", "Repairing", "Loading", "Checking"]
    adjective = ["master", "radiant", "silent", "harmonic", "fast"]
    noun = ["solar array", "particle reshaper", "cosmic ray", "orbiter", "bit"]
    message = ""
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = "{0} {1} {2}...".format(
                random.choice(verb), random.choice(adjective), random.choice(noun)
            )
            self.update_state(
                state="PROGRESS", meta={"current": i, "total": total, "status": message}
            )
        time.sleep(0.5)
    return {"current": 100, "total": 100, "status": "Task completed!", "result": 42}


@celery.task
def log(message):
    logger.debug(message)
    logger.info(message)
    logger.warning(message)
    logger.error(message)
    logger.critical(message)