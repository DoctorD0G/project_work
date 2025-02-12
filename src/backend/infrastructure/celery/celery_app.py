import sentry_sdk
from celery import Celery, signals
from celery import Task
from sentry_sdk.integrations.celery import CeleryIntegration

from infrastructure.celery.celery_config import imports as celery_modules
from infrastructure.celery.config import celery_settings
from infrastructure.container import init_container

container = init_container()


class DBSessionTask(Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        container.wire(modules=celery_modules)
        return self.run(*args, **kwargs)


celery = Celery(
    "service", broker=celery_settings.TASK_BROKER_URL, task_cls=DBSessionTask
)
celery.config_from_object("infrastructure.celery.celery_config")


@signals.celeryd_init.connect
def init_sentry(**_kwargs):
    sentry_sdk.init(
        dsn=celery_settings.SENTRY_DSN,
        environment=celery_settings.SENTRY_ENVIRONMENT,
        traces_sample_rate=celery_settings.SENTRY_TRACES_SAMPLE_RATE,
        send_default_pii=True,
        integrations=[
            CeleryIntegration(
                monitor_beat_tasks=True,
            ),
        ],
    )
