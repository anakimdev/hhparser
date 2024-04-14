from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, BigInteger, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(nullable=False)
    address: Mapped[Text] = mapped_column(Text(), nullable=True)

    role: Mapped['Role'] = relationship(baweckref="role")


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class Templates(Base):
    __tablename__ = "template"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    profession: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(50), default='все')
    salary: Mapped[int] = mapped_column(Integer(), nullable=False)

    user_id: Mapped['User'] = relationship(backref='template')


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    site: Mapped[str] = mapped_column(Text(), nullable=True)
#
# class Banner(Base):
#     __tablename__ = 'banner'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(15), unique=True)
#     image: Mapped[str] = mapped_column(String(150), nullable=True)
#     description: Mapped[str] = mapped_column(Text, nullable=True)
#
#
# class Category(Base):
#     __tablename__ = 'category'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#
#
# class Product(Base):
#     __tablename__ = 'product'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(150), nullable=False)
#     description: Mapped[str] = mapped_column(Text)
#     price: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
#     image: Mapped[str] = mapped_column(String(150))
#     category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
#
#     category: Mapped['Category'] = relationship(backref='product')
#
#
# class User(Base):
#     __tablename__ = 'user'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
#     first_name: Mapped[str] = mapped_column(String(150), nullable=True)
#     last_name: Mapped[str]  = mapped_column(String(150), nullable=True)
#     phone: Mapped[str]  = mapped_column(String(13), nullable=True)
#
#
# class Cart(Base):
#     __tablename__ = 'cart'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
#     product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
#     quantity: Mapped[int]
#
#     user: Mapped['User'] = relationship(backref='cart')
#     product: Mapped['Product'] = relationship(backref='cart')
