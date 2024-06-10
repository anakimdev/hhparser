from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base, idpk


class ProfessionCategoriesTable(Base):
    __tablename__ = "profession_categories"

    id: Mapped[idpk]
    api_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]

    professions: Mapped[list["ProfessionsTable"]] = relationship(
        back_populates="categories",
        secondary="professions_and_categories",
    )

    __table_args__ = (
        Index('profession_cat_idx', 'api_id'),
    )