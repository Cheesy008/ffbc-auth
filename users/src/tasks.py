from .core.celery import celery_app


@celery_app.task
def celery_test():
    print("WORKS")
