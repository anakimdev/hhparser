from typing import Optional

from sqlalchemy import String, ForeignKey, Integer, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import idpk, created_at, updated_at, Base


profession_vacancy_association = Table(
    'profession_vacancy_associations',
    Base.metadata,
    Column('profession_id', Integer, ForeignKey('professions.api_id')),
    Column('vacancy_id', Integer, ForeignKey('vacancies.api_id'))

)


class VacanciesTable(Base):
    __tablename__ = "vacancies"

    id: Mapped[idpk]
    api_id: Mapped[int]
    name: Mapped[str]
    area_id: Mapped[int] = ForeignKey("areas.api_id")
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
        back_populates="vacancy",
        secondary=profession_vacancy_association
    )


