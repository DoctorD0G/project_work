from typing import Tuple, List

from domain.entities.common import EntityId, Total
from domain.entities.task import (
    TaskEntity,
    CreateTask,
    UpdateTask,
)
from domain.repositories.base import Filter
from domain.repositories.task import TaskRepositoryInterface


class MockTaskRepository(TaskRepositoryInterface):

    def convert_model_to_entity(self, *args, **kwargs):
        pass

    async def create(self, obj_in: CreateTask) -> TaskEntity:
        self.task_e = TaskEntity(id=1, **obj_in.__dict__)
        return self.task_e

    async def get(self, id: EntityId) -> TaskEntity | None:
        return self.task_e if hasattr(self, "task_e") else None

    async def get_one_by_filter(self, filter: Filter) -> TaskEntity | None:
        return self.task_e

    async def update(self, id: EntityId, obj_in: UpdateTask) -> TaskEntity | None:
        self.task_e = TaskEntity(**obj_in.__dict__)
        return self.task_e

    async def delete(self, id: EntityId):
        del self.task_e

    async def delete_by_filter(self, filter: Filter) -> int:
        del self.task_e
        return 1

    async def get_paginable_items(
        self,
        page: int,
        size: int,
        sort_field: str | None = None,
        sort_descending: bool | None = None,
        filter: Filter | None = None,
    ) -> Tuple[List[TaskEntity], Total]:
        return [self.task_e], Total(1)

    async def get_filtered_items(
        self,
        sort_field: str | None = None,
        sort_descending: bool | None = None,
        filter: Filter | None = None,
        limit: int | None = None,
    ) -> list[TaskEntity]:
        return [self.task_e]
