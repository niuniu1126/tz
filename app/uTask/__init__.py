from celery import Celery
from kombu import Queue, Exchange
from app.uTask import celery_config

celery = Celery('tz')

celery.config_from_object(celery_config)


celery.conf.task_queues = [Queue('celery', Exchange('celery'),
                                 routing_key='celery', queue_arguments={'x-max-priority': 10})]