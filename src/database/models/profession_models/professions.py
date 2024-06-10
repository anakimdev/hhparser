from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base, idpk


class ProfessionsTable(Base):
    __tablename__ = "professions"

    id: Mapped[idpk]
    api_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]

    categories: Mapped[list["ProfessionCategoriesTable"]] = relationship(
        back_populates="professions",
        secondary="professions_and_categories",
    )

    vacancies: Mapped[list["VacanciesTable"]] = relationship(
        back_populates="professional_roles",
        secondary="professions_and_vacancies",
    )

    __table_args__ = (
        Index('profession_api_idx', 'api_id'),
    )




