from dependency_injector import containers, providers

from application.services.app_manager import AppManagerService
from application.services.task import TaskService
from infrastructure.permissions import permissions
from infrastructure.repositories.config import db_settings

from infrastructure.schemas.user import (
    CreateUserDto,
    UpdateUserDto,
    UserFilterDto,
    UserDto,
    ResponseUserDto,
)

# ----------------------------------- START POSTGRESQL -------------------------------------------------------------------
from infrastructure.repositories.psql.db import Database
from infrastructure.repositories.psql.models.user import UserModel, RoleModel

from infrastructure.repositories.psql.repositories.app_manager import (
    AppManagerSqlAlchemyRepository,
)
from infrastructure.repositories.psql.repositories.task import TaskSqlAlchemyRepository

#                    --------------- postgresql  token auth --------------------------------------------------------------
from cism_fastapi_user.containers import PsqlContainerSettings, PsqlUserContainer

fastapi_user_settings = PsqlContainerSettings(
    token_expire=720,
    secret_key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    user_model=UserModel,
    role_model=RoleModel,
    permissions=permissions,
    user_schema=UserDto,
    create_schema=CreateUserDto,
    update_schema=UpdateUserDto,
    user_filter_schema=UserFilterDto,
    user_response_schema=ResponseUserDto,
)
# ----------------------------------- END POSTGRESQL ---------------------------------------------------------------------


# ----------------------------------- END MONGODB ----------------------------------------------------------------------


class Container(containers.DeclarativeContainer):

    psql_db_client = providers.Singleton(
        Database, db_url=db_settings.DATABASE_URL, pool_size=64
    )
    task_repository = providers.Factory(
        TaskSqlAlchemyRepository, session_contextmanager=psql_db_client.provided.session
    )
    app_manager_repository = providers.Factory(
        AppManagerSqlAlchemyRepository,
        session_contextmanager=psql_db_client.provided.session,
    )
    fastapi_user_container = providers.Container(
        PsqlUserContainer,
        session_contextmanager=psql_db_client.provided.session,
    )

    task_service = providers.Factory(TaskService, task_repository=task_repository)
    app_manager_service = providers.Factory(
        AppManagerService, app_manager_repository=app_manager_repository
    )
    fastapi_user_container.config.from_dict(fastapi_user_settings.model_dump())


def init_container():
    container = Container()
    container.init_resources()
    return container
