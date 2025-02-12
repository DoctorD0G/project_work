from cism_fastapi_user.defaults.permissions import (
    DEFAULT_PERMISSIONS as CISM_USER_PERMISSIONS,
)
from cism_fastapi_user.schemas.auth import PermissionDto

APP_SETTINGS_VIEW_PERMISSION = PermissionDto(
    name="app_settings:read", title="Настройки сервиса: просмотр"
)
APP_SETTINGS_EDIT_PERMISSION = PermissionDto(
    name="app_settings:edit", title="Настройки сервиса: управление"
)
TASK_VIEW_PERMISSION = PermissionDto(name="task:read", title="Задачи: просмотр")
TASK_EDIT_PERMISSION = PermissionDto(name="task:edit", title="Задачи: управление")

permissions = [
    APP_SETTINGS_VIEW_PERMISSION,
    APP_SETTINGS_EDIT_PERMISSION,
    TASK_VIEW_PERMISSION,
    TASK_EDIT_PERMISSION,
] + CISM_USER_PERMISSIONS
