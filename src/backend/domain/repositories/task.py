from abc import ABC

from domain.entities.task import (
    TaskEntity,
    UpdateTask,
    CreateTask,
)
from domain.repositories.base import AbstractRepository, ModelType


class TaskRepositoryInterface(
    AbstractRepository[
        ModelType,
        CreateTask,
        UpdateTask,
        TaskEntity,
    ],
    ABC,
): ...
