from logging import getLogger

import pytest

from application.services.task import TaskService
from domain.entities.task import CreateTask, TaskEntity

logger = getLogger(__name__)


@pytest.fixture()
def task_service(dependencies) -> TaskService:
    yield dependencies.task_service()


class TestTask:
    task_name = "test"

    @pytest.mark.asyncio
    async def test_task(self, task_service: TaskService) -> None:
        task_e: TaskEntity = await task_service.create_task(
            create_task=CreateTask(name=self.task_name)
        )
        assert task_e.name == self.task_name, "Ошибка создания задачи"

        task_e: TaskEntity = await task_service.task_detail(id=1)
        assert task_e.name == self.task_name, "Ошибка получения задачи"

        tasks, count = await task_service.get_paginable_tasks(page=1, size=10)
        assert count == 1, "Ошибка получения задач"

        await task_service.delete_task(id=1)
        task_e: None = await task_service.task_detail(id=1)
        assert task_e is None, "Ошибка удаления задачи"
