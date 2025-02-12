from domain.entities.task import TaskEntity
from pydantic import ConfigDict


class DbTaskEntity(TaskEntity):
    model_config = ConfigDict(
        from_attributes=True,
    )
