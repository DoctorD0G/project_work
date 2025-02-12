from enum import IntEnum, unique

from pydantic import BaseModel


@unique
class AppStatus(IntEnum):
    DEBUGGING = 1
    PAUSING = 5
    RUNNING = 10


class AppSettingsEntity(BaseModel):
    status: AppStatus
