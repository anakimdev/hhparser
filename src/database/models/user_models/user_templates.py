from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import idpk, Base


class UserTemplatesTable(Base):
    __tablename__ = "user_templates"

    id: Mapped[idpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    profession: Mapped[str]
    expected_salary: Mapped[int]
    region: Mapped[str]

    user: Mapped["UsersTable"] = relationship(
        "UsersTable",
        back_populates='templates',
    )


