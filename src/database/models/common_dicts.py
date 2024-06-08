from typing import Optional

from sqlalchemy import ForeignKey, Table, Integer, Column, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base, idpk, str_256


class WorkloadsTable(Base):
    __tablename__ = "workloads"

    id: Mapped[idpk]
    key: Mapped[str_256]
    title: Mapped[str_256]


class IndustryCategoriesTable(Base):
    __tablename__ = "industry_categories"

    id: Mapped[idpk]
    name: Mapped[str]

    industries: Mapped[list["IndustriesTable"]] = relationship(
        back_populates="category"
    )


class IndustriesTable(Base):
    __tablename__ = "industries"

    id: Mapped[idpk]
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("industry_categories.id"))

    category: Mapped["IndustryCategoriesTable"] = relationship(
        back_populates="industries"
    )


class AreasTable(Base):
    __tablename__ = "areas"

    id: Mapped[idpk]
    name: Mapped[str]
    api_id: Mapped[int] = mapped_column(unique=True)

    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('areas.api_id'))

    parent: Mapped["AreasTable"] = relationship(
        backref='children',
        remote_side='AreaTable.api_id'
    )

    __table_args__ = (
        Index('api_index', 'api_id'),
    )


class RolesTable(Base):
    __tablename__ = "roles"

    id: Mapped[idpk]
    title: Mapped[str_256]

    users: Mapped[list["UsersTable"]] = relationship(
        back_populates='role'
    )
