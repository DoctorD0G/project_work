from datetime import datetime
from domain.entities.app_manager import AppStatus
from infrastructure.repositories.config import db_settings
from infrastructure.repositories.psql.db import Base
from sqlalchemy import Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class AppSettingsModel(Base):
    __tablename__ = "app_settings"
    __table_args__ = {"schema": db_settings.DB_SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[int] = mapped_column(
        Integer,
        default=AppStatus.RUNNING,
        server_default=f"{AppStatus.RUNNING}",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=datetime.now()
    )
