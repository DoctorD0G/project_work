from abc import ABC, abstractmethod

from domain.entities.app_manager import AppSettingsEntity


class AppManagerRepositoryInterface(ABC):
    @abstractmethod
    async def get_app_settings(self) -> AppSettingsEntity | None:
        """
        Получить настройку приложения
        :return: настройка приложения
        """
        raise NotImplementedError

    @abstractmethod
    async def create_default_app_settings(self) -> AppSettingsEntity:
        """
        Создание настройки по умолчанию (дефолтной)
        :return: настройка приложения
        """
        raise NotImplementedError

    @abstractmethod
    async def update_app_settings(self, app_settings_e: AppSettingsEntity) -> None:
        """
        Обновление настройки приложения
        :return:
        """
        raise NotImplementedError
