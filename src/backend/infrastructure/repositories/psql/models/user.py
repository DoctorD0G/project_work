from sqlalchemy import DateTime, func
from datetime import datetime
from infrastructure.repositories.config import db_settings
from infrastructure.repositories.psql.db import Base
from sqlalchemy.orm import Mapped, mapped_column

from cism_fastapi_user.db.models.psql import BaseUserModel, BaseRoleModel


class UserModel(BaseUserModel, Base):
    __tablename__ = "user_table"
    __table_args__ = {"schema": db_settings.DB_SCHEMA}

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=datetime.now()
    )


class RoleModel(BaseRoleModel, Base):
    __tablename__ = "user_role_table"
    __table_args__ = {"schema": db_settings.DB_SCHEMA}

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=datetime.now()
    )
