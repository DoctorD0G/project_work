from domain.entities.task import (
    TaskEntity,
    CreateTask,
    UpdateTask,
)
from domain.repositories.base import SQLAlchemyRepository
from domain.repositories.task import TaskRepositoryInterface
from infrastructure.repositories.psql.models.task import TaskModel


class TaskSqlAlchemyRepository(
    SQLAlchemyRepository[
        TaskModel,
        CreateTask,
        UpdateTask,
        TaskEntity,
    ],
    TaskRepositoryInterface,
):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, model=TaskModel, entity=TaskEntity, **kwargs)
