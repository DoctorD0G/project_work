import asyncio

from dependency_injector.wiring import inject, Provide

from common.logs import logger
from domain.services.app_manager import AppManagerServiceInterface
from domain.services.task import TaskServiceInterface
from infrastructure.celery.celery_app import celery
from infrastructure.container import Container


@inject
async def async_test_task(
    task_service: TaskServiceInterface = Provide[Container.task_service],
    app_manager_service: AppManagerServiceInterface = Provide[
        Container.app_manager_service
    ],
):
    if await app_manager_service.is_app_on_pause():
        return

    logger.error(task_service)
    logger.error(await task_service.get_paginable_tasks(1, 10))


@celery.task(bind=True)
def test_task(self):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_test_task())
