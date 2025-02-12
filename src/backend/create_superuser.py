import argparse
import asyncio

from cism_fastapi_user.schemas.user import CreateUserDto
from dependency_injector.wiring import inject

from infrastructure.web.app import container, fastapi_user_container

parser = argparse.ArgumentParser(description="create user script")
parser.add_argument("-u", dest="username", required=True)
parser.add_argument("-p", dest="passwd", required=True)


@inject
async def db_create_superuser(
    username: str,
    password: str,
):
    user_service = fastapi_user_container.user_service()
    await user_service.create_user(
        CreateUserDto(fio="", password=password, username=username, is_admin=True)
    )


if __name__ == "__main__":
    args = parser.parse_args()

    if args.username and args.passwd:
        asyncio.run(db_create_superuser(args.username, args.passwd))

container.wire(packages=[__name__])
