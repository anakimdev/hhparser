from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base, idpk, str_256


class WorkloadTable(Base):
    __tablename__ = "workloads"

    id: Mapped[idpk]
    key: Mapped[str_256]
    title: Mapped[str_256]


class IndustryCategoryTable(Base):
    __tablename__ = "industry_categories"

    id: Mapped[idpk]
    name: Mapped[str]

    industries: Mapped[list["IndustryTable"]] = relationship(
        back_populates="category"
    )


class IndustryTable(Base):
    __tablename__ = "industries"

    id: Mapped[idpk]
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("industry_categories.id"))

    category: Mapped["IndustryCategoryTable"] = relationship(
        back_populates="industries"
    )


