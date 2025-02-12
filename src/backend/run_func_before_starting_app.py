import asyncio

from dependency_injector.wiring import inject

from infrastructure.web.app import container, fastapi_user_container


@inject
async def main():
    # проверка прав. удаляются несуществующие права в ролях
    role_service = fastapi_user_container.role_service()
    await role_service.permission_check_and_cleanup()


if __name__ == "__main__":
    asyncio.run(main())

container.wire(packages=[__name__])
