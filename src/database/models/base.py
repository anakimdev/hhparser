from datetime import datetime
from typing import Annotated

from sqlalchemy import text, String
from sqlalchemy.orm import DeclarativeBase, mapped_column


idpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_256 = Annotated[str, mapped_column(String(256))]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now()) + interval '1 day'"),
    onupdate=datetime.utcnow)]




class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = ()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"

