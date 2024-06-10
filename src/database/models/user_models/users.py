from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database.models.base import Base, idpk, created_at, updated_at


class UsersTable(Base):
    __tablename__ = "users"

    id: Mapped[idpk]
    nickname: Mapped[str]
    telegram_id: Mapped[int]
    roles_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    role: Mapped["RolesTable"] = relationship(
        "RolesTable",
        back_populates='users',
    )

    templates: Mapped[list["UserTemplatesTable"]] = relationship(
        back_populates='user',
    )
