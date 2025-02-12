from domain.entities.app_manager import AppSettingsEntity
from pydantic import ConfigDict


class DbAppSettingsEntity(AppSettingsEntity):
    model_config = ConfigDict(from_attributes=True)
