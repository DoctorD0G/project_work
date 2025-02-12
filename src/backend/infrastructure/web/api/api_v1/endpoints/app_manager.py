import logging
from typing import Any

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from domain.entities.app_manager import AppSettingsEntity
from domain.services.app_manager import AppManagerServiceInterface
from infrastructure.container import Container
from infrastructure.permissions import (
    APP_SETTINGS_VIEW_PERMISSION,
    APP_SETTINGS_EDIT_PERMISSION,
)
from infrastructure.web.api.dependencies import perm_check

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", summary="Настройки приложения")
@perm_check(APP_SETTINGS_VIEW_PERMISSION)
@inject
async def get_app_settings(
    app_manager_service: AppManagerServiceInterface = Depends(
        Provide[Container.app_manager_service]
    ),
) -> Any:
    try:
        return await app_manager_service.get_app_settings()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка получения настроек приложения: {e}",
        ) from e


@router.put("/")
@perm_check(APP_SETTINGS_EDIT_PERMISSION)
@inject
async def set_app_settings(
    app_settings_e: AppSettingsEntity,
    app_manager_service: AppManagerServiceInterface = Depends(
        Provide[Container.app_manager_service]
    ),
) -> Any:
    try:
        await app_manager_service.update_app_settings(app_settings_e)
        return app_settings_e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка изменения настроек приложения: {e}",
        ) from e
