from celery import Celery

from create_app import create_app
from apps.extensions import celery

create_app()
