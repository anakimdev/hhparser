from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.database.models.base import Base


class ProfessionsAndCategoriesTable(Base):
    __tablename__ = "professions_and_categories"

    profession_id: Mapped[int] = mapped_column(ForeignKey("professions.api_id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("profession_categories.api_id"), primary_key=True)

