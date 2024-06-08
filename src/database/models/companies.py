from datetime import datetime
from sqlalchemy.orm import Mapped

from src.database.models.base import Base, idpk


class CompaniesTable(Base):
    __tablename__ = "companies"

    id: Mapped[idpk]
    title: Mapped[str]
    address: Mapped[str]

    okved: Mapped[str]
    inn: Mapped[int]
    ogrn: Mapped[int]
    kpp: Mapped[int]

    formation_method: Mapped[str]
    registration_date: Mapped[datetime]
    accounting_date: Mapped[datetime]

    capital: Mapped[str]
    msp_subject: Mapped[str]