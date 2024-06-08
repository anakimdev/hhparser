from sqlalchemy import Table, Column, ForeignKey, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base, idpk

profession_category_associations = Table(
    "profession_category_associations",
    Base.metadata,
    Column("category_id", Integer, ForeignKey("profession_categories.api_id")),
    Column("profession_id", Integer, ForeignKey("professions.api_id")),
)


class ProfessionCategoriesTable(Base):
    __tablename__ = "profession_categories"

    id: Mapped[idpk]
    api_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]

    professions: Mapped[list["ProfessionsTable"]] = relationship(
        back_populates="categories",
        secondary=profession_category_associations
    )

    __table_args__ = (
        Index('api_index', 'api_id')
    )


class ProfessionsTable(Base):
    __tablename__ = "professions"

    id: Mapped[idpk]
    api_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]

    categories: Mapped[list['ProfessionCategoriesTable']] = relationship(
        back_populates="professions",
        secondary=profession_category_associations
    )

    __table_args__ = (
        Index('api_index', 'api_id')
    )
