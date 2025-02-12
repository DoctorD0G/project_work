from cism_fastapi_user.schemas.rest import ResponseUserDto as BaseResponseUserDto
from cism_fastapi_user.schemas.user import (
    CreateUserDto as BaseCreateUserDto,
    UserFilterDto as BaseUserFilterDto,
    UpdateUserDto as BaseUpdateUserDto,
    UserDto as BaseUserDto,
)
from cism_fastapi_user.schemas.role import RoleDto as BaseRoleDto


class UpdateUserDto(BaseUpdateUserDto): ...


class CreateUserDto(BaseCreateUserDto): ...


class UserFilterDto(BaseUserFilterDto): ...


class ResponseUserDto(BaseResponseUserDto): ...


class UserDto(BaseUserDto): ...


class RoleDto(BaseRoleDto): ...
