from celery.schedules import crontab
from infrastructure.celery.config import celery_settings
from kombu import Queue

imports = ("infrastructure.celery.tasks.periodic",)

accept_content = ["json", "msgpack", "yaml"]
task_serializer = "json"
result_serializer = "json"
enable_utc = False

broker_pool_limit = 1
worker_prefetch_multiplier = 1
broker_heartbeat = None
broker_connection_timeout = 40
broker_connection_retry_on_startup = True

beat_schedule = {
    "test-task": {
        "task": "infrastructure.celery.tasks.periodic.test_task",
        "schedule": crontab(minute="*/1"),
        "options": {"queue": celery_settings.PERIODIC_WORKER_QUEUE_NAME},
    },
}

task_queues = [
    Queue(
        celery_settings.PERIODIC_WORKER_QUEUE_NAME,
        routing_key=celery_settings.PERIODIC_WORKER_QUEUE_NAME,
    ),
]

task_routes = {
    "infrastructure.celery.tasks.periodic.*": {
        "queue": celery_settings.PERIODIC_WORKER_QUEUE_NAME
    },
}
