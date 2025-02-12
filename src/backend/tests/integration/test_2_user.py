from logging import getLogger

import pytest
from infrastructure.schemas.user import CreateUserDto, UserFilterDto

logger = getLogger(__name__)


@pytest.fixture()
def user_service(dependencies):
    user_service = dependencies.fastapi_user_container.user_service()
    yield user_service


class TestUsersService:
    username = "admin"
    password = "admin"
    fio = "FIO"
    email = "test@mail.ru"

    @pytest.mark.asyncio
    async def test_create_user(self, user_service) -> None:
        await user_service.create_user(
            CreateUserDto(
                fio=self.fio,
                password=self.password,
                username=self.username,
                is_admin=True,
            )
        )
        users = await user_service.get_users(UserFilterDto(username=self.username))

        assert len(users) == 1
