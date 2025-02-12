from typing import Callable, AsyncContextManager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.app_manager import AppSettingsEntity, AppStatus
from domain.repositories.app_manager import AppManagerRepositoryInterface
from infrastructure.repositories.psql.models.app_manager import AppSettingsModel
from infrastructure.repositories.psql.schemas.app_manager import DbAppSettingsEntity


class AppManagerSqlAlchemyRepository(AppManagerRepositoryInterface):
    session_contextmanager: Callable[..., AsyncContextManager[AsyncSession]] = None

    def __init__(
        self,
        session_contextmanager: Callable[..., AsyncContextManager[AsyncSession]],
    ):
        super().__init__()
        self.session_contextmanager = session_contextmanager

    async def create_default_app_settings(self) -> AppSettingsEntity | None:
        """
        Создание настройки по умолчанию (дефолтной)
        :return: настройка приложения
        """
        async with self.session_contextmanager() as db_session:
            app_settings_m = AppSettingsModel(status=AppStatus.PAUSING)
            db_session.add(app_settings_m)
            await db_session.commit()
            await db_session.refresh(app_settings_m)
            return DbAppSettingsEntity.model_validate(app_settings_m)

    async def get_app_settings(self) -> AppSettingsEntity | None:
        """
        Получить настройку приложения
        :return: настройка приложения
        """
        async with self.session_contextmanager() as db_session:
            query = select(AppSettingsModel).limit(1)
            app_settings_m = (await db_session.execute(query)).scalars().first()
            return (
                DbAppSettingsEntity.model_validate(app_settings_m)
                if app_settings_m
                else None
            )

    async def update_app_settings(self, app_settings_e: AppSettingsEntity) -> None:
        """
        Обновление настройки приложения
        :return:
        """
        async with self.session_contextmanager() as db_session:
            query = select(AppSettingsModel).limit(1)
            app_settings_m = (await db_session.execute(query)).scalars().first()
            app_settings_m.status = app_settings_e.status
            await db_session.commit()
