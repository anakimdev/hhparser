from typing import Optional

from sqlalchemy import ForeignKey, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import idpk, Base, created_at, updated_at


class VacanciesTable(Base):
    __tablename__ = "vacancies"

    id: Mapped[idpk]
    api_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]
    area_id: Mapped[int] = mapped_column(ForeignKey("areas.api_id"))
    employer: Mapped[str]
    has_salary: Mapped[bool]
    salary_from: Mapped[Optional[int]]
    salary_to: Mapped[Optional[int]]
    currency: Mapped[Optional[str]] = mapped_column(String(3))
    experience: Mapped[str]
    schedule: Mapped[str]
    published_at: Mapped[created_at]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    professional_roles: Mapped[list["ProfessionsTable"]] = relationship(
        back_populates="vacancies",
        secondary="professions_and_vacancies",
    )

    area: Mapped["AreasTable"] = relationship(
        back_populates="vacancies",
        remote_side="AreasTable.api_id",
    )


    __table_args__ = (
        Index("vacancy_api_idx", "api_id"),
    )
