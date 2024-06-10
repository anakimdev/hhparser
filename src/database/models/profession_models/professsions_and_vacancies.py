from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class ProfessionsAndVacanciesTable(Base):
    __tablename__ = "professions_and_vacancies"

    vacancy_id: Mapped[int] = mapped_column(ForeignKey('vacancies.api_id'), primary_key=True)
    profession_id: Mapped[int] = mapped_column(ForeignKey('professions.api_id'), primary_key=True)

