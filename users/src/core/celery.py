from celery import Celery
from .config import settings


REDIS_URL = "redis://{0}:{1}/0".format(settings.REDIS_HOST, settings.REDIS_PORT)

celery_app = Celery(__name__)
celery_app.autodiscover_tasks(["src.tasks"])

celery_app.conf.broker_url = REDIS_URL
celery_app.conf.result_backend = REDIS_URL
celery_app.conf.accept_content = ["json"]
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
