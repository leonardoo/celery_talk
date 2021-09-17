import os

BASEDIR = os.path.abspath(os.path.dirname(__name__))
SQLITE_DB = "sqlite:///" + os.path.join(BASEDIR, "db.sqlite")


class Config(object):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(16).hex())
    BROKER_URL = os.getenv("BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND = os.getenv(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/1"
    )


class DevelopmentConfig(Config):
    DEBUG = True


config = DevelopmentConfig
