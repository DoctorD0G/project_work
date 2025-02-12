from abc import ABC, abstractmethod

from domain.entities.app_manager import AppSettingsEntity
from domain.repositories.app_manager import AppManagerRepositoryInterface


class AppManagerServiceInterface(ABC):
    def __init__(
        self,
        app_manager_repository: AppManagerRepositoryInterface,
    ):
        self.app_manager_repository = app_manager_repository

    @abstractmethod
    async def get_app_settings(self) -> AppSettingsEntity:
        """
        Получить настройку приложения
        :return: настройка приложения
        """
        raise NotImplementedError

    @abstractmethod
    async def update_app_settings(self, app_settings_e: AppSettingsEntity) -> bool:
        """
        Обновление настройки приложения
        :return: булево значение статуса обновления
        """
        raise NotImplementedError

    @abstractmethod
    async def is_app_on_pause(self) -> bool:
        """
        Приложение на паузе
        :return: булево значение
        """
        raise NotImplementedError

    @abstractmethod
    async def is_app_on_debug(self) -> bool:
        """
        Приложение в режиме отладки
        :return: булево значение
        """
        raise NotImplementedError

    @abstractmethod
    async def is_app_on_running(self) -> bool:
        """
        Приложение в режиме работы
        :return: булево значение
        """
        raise NotImplementedError
