from datetime import datetime

from pydantic import BaseModel

from domain.entities.common import EntityId


class BaseTask(BaseModel):
    name: str


class TaskEntity(BaseTask):
    id: EntityId
    created_at: datetime
    updated_at: datetime | None = None


class CreateTask(BaseTask):
    created_at: datetime | None = None


class UpdateTask(BaseTask):
    id: EntityId
    updated_at: datetime | None = None


class PaginableTaskFilter(BaseModel):
    name: str | None = None
