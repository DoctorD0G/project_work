from domain.entities.app_manager import AppSettingsEntity, AppStatus
from domain.services.app_manager import AppManagerServiceInterface


class AppManagerService(AppManagerServiceInterface):
    async def get_app_settings(self) -> AppSettingsEntity:
        """
        Получить настройку приложения
        :return: настройка приложения
        """
        app_settings_e = await self.app_manager_repository.get_app_settings()
        if not app_settings_e:
            app_settings_e = (
                await self.app_manager_repository.create_default_app_settings()
            )
        return app_settings_e

    async def update_app_settings(self, app_settings_e: AppSettingsEntity) -> bool:
        """
        Обновление настройки приложения
        :return: булево значение статуса обновления
        """
        await self.app_manager_repository.update_app_settings(app_settings_e)
        return True

    async def is_app_on_pause(self) -> bool:
        """
        Приложение на паузе
        :return: булево значение
        """
        return (await self.get_app_settings()).status == AppStatus.PAUSING

    async def is_app_on_debug(self) -> bool:
        """
        Приложение в режиме отладки
        :return: булево значение
        """
        return (await self.get_app_settings()).status == AppStatus.DEBUGGING

    async def is_app_on_running(self) -> bool:
        """
        Приложение в режиме работы
        :return: булево значение
        """
        return (await self.get_app_settings()).status == AppStatus.RUNNING
