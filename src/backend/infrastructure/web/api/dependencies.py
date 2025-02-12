from functools import wraps

from cism_fastapi_user.schemas.auth import PermissionDto
from cism_fastapi_user.schemas.user import UserDto
from cism_fastapi_user.services.auth import oauth2_scheme
from cism_python_utils.base.fastapi_wraps import fastapi_wraps
from dependency_injector.wiring import inject, Provide
from fastapi import Depends, HTTPException

from infrastructure.container import Container


def perm_check(permission: PermissionDto):
    def decorator(function):
        @fastapi_wraps(function)
        @inject
        async def wrapper(
            token: str = Depends(oauth2_scheme),
            user_auth_service=Depends(
                Provide[Container.fastapi_user_container.auth_service]
            ),
            *args,
            **kwargs
        ):
            has_perm_fun = user_auth_service.user_has_permission(permission)
            await has_perm_fun(token)
            return await function(*args, **kwargs)

        return wrapper

    return decorator


@inject
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service=Depends(Provide[Container.fastapi_user_container.auth_service]),
) -> UserDto | None:
    user_dto = await auth_service.get_user_by_token(token)
    return user_dto


def app_status_paused(func):
    @wraps(func)
    @inject
    async def wrapper(
        app_manager_service=Depends(Provide[Container.app_manager_service]),
        *args,
        **kwargs
    ):
        """
        Декоратор для проверки статуса приложения.

        Этот декоратор используется для блокировки выполнения определенных операций, если статус
        приложения установлен как "Pausing".
        """

        if await app_manager_service.is_app_on_pause():
            raise HTTPException(
                status_code=503,
                detail="Вы не можете выполнить это действие, когда сервис приостановлен",
            )

        return await func(*args, **kwargs)

    return wrapper
