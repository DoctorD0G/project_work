from logging import getLogger

import pytest

from application.services.app_manager import AppManagerService
from domain.entities.app_manager import AppStatus, AppSettingsEntity

logger = getLogger(__name__)


@pytest.fixture()
def app_manager(dependencies) -> AppManagerService:
    yield dependencies.app_manager_service()


class TestAppManager:
    @pytest.mark.asyncio
    async def test_app_manager_init_state(self, app_manager: AppManagerService) -> None:
        app_settings = await app_manager.get_app_settings()

        assert app_settings.status == AppStatus.PAUSING

    @pytest.mark.asyncio
    async def test_app_manager_change_state(
        self, app_manager: AppManagerService
    ) -> None:
        await app_manager.update_app_settings(
            AppSettingsEntity(status=AppStatus.RUNNING)
        )
        app_settings = await app_manager.get_app_settings()
        assert app_settings.status == AppStatus.RUNNING
