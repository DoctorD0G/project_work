from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from domain.entities.common import Total, EntityId
from domain.entities.task import (
    TaskEntity,
    CreateTask,
    UpdateTask,
    PaginableTaskFilter,
)
from domain.repositories.task import TaskRepositoryInterface


class TaskServiceInterface(ABC):
    @abstractmethod
    def __init__(
        self,
        task_repository: TaskRepositoryInterface,
    ):
        self.task_repository = task_repository

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    async def task_detail(self, id: EntityId) -> TaskEntity | None:
        """
        Получение задачи по идентификатору
        :param id: идентификатор задачи
        :return: инфомрация о задаче
        """
        raise NotImplementedError

    @abstractmethod
    async def create_task(self, task: CreateTask) -> TaskEntity:
        """
        Добавление задачи
        :param create_task_e: данные для создания задачи
        :return: информация о задаче
        """
        raise NotImplementedError

    @abstractmethod
    async def update_task(self, update_task: UpdateTask) -> TaskEntity | None:
        """
        Обновление задачи
        :param update_task_e: данные для обновления задачи
        :return: инфомрация о задаче
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, id: EntityId) -> bool:
        """
        Удаление задачи
        :param id: идентификатор задачи
        :return: инфомрация об удалении
        """
        raise NotImplementedError
