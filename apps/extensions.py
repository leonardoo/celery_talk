from celery import Celery

celery = Celery("workers")


def register_extensions(app):
    # load celery config
    celery.conf.update(
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        broker_url=app.config["BROKER_URL"],
    )
    #celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
