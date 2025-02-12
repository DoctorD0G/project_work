from datetime import datetime
from typing import List, Optional, Tuple

from application.validators.task import TaskValidator
from domain.entities.common import Total, EntityId
from domain.entities.task import (
    TaskEntity,
    CreateTask,
    UpdateTask,
    PaginableTaskFilter,
)
from domain.repositories.base import Filter, FieldFilter, FilterOperator
from domain.repositories.task import TaskRepositoryInterface
from domain.services.task import TaskServiceInterface


class TaskService(TaskServiceInterface):
    def __init__(
        self,
        task_repository: TaskRepositoryInterface,
    ):
        super().__init__(task_repository)

    async def get_paginable_tasks(
        self,
        page: int,
        size: int,
        sort_field: Optional[str] = None,
        sort_descending: Optional[bool] = None,
        paginable_filter: Optional[PaginableTaskFilter] = None,
    ) -> Tuple[List[TaskEntity], Total]:
        """
        Постраничное получение задач
        :param page: номер страницы
        :param size: кол-во эл. на странице
        :param sort_field:  поле для сортировки
        :param sort_descending: сортировать по убыванию
        :param paginable_filter: фильтр
        :return: список задач и кол-во задач согласно фильтра
        """
        filter = None
        if paginable_filter and paginable_filter.name:
            filter = Filter(
                filters=[
                    FieldFilter(
                        field="name",
                        operator=FilterOperator.ILIKE,
                        value=paginable_filter.name,
                    ),
                ]
            )
        return await self.task_repository.get_paginable_items(
            page, size, sort_field, sort_descending, filter=filter
        )

    async def task_detail(self, id: EntityId) -> TaskEntity | None:
        """
        Получение задачи по идентификатору
        :param id: идентификатор задачи
        :return: инфомрация о задаче
        """
        return await self.task_repository.get(id)

    async def create_task(self, create_task: CreateTask) -> TaskEntity:
        """
        Добавление задачи
        :param create_task_e: данные для создания задачи
        :return: информация о задаче
        """
        TaskValidator.validate_name(create_task.name)

        create_task.created_at = datetime.now()
        task_e = await self.task_repository.create(create_task)
        return task_e

    async def update_task(self, update_task: UpdateTask) -> TaskEntity | None:
        """
        Обновление задачи
        :param update_task_e: данные для обновления задачи
        :return: инфомрация о задаче
        """
        TaskValidator.validate_name(update_task.name)

        update_task.updated_at = datetime.now()
        result = await self.task_repository.update(update_task.id, update_task)
        return result

    async def delete_task(self, id: EntityId) -> bool:
        """
        Удаление задачи
        :param id: идентификатор задачи
        :return: инфомрация об удалении
        """
        result = await self.task_repository.delete(id)
        return result
