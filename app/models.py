import datetime

from sqlalchemy import DateTime, Integer, Float, String, func, ForeignKey
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, WriteOnlyMapped, relationship

from config import PG_DSN

engine = create_async_engine(
    PG_DSN,
)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


class Advertisement(Base):
    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    price: Mapped[float] = mapped_column(Float, default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "price": self.price,
        }


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    # password: Mapped[str] = mapped_column(String(72), nullable=False)
    advertisements: WriteOnlyMapped['Advertisement'] = relationship('Advertisement', backref='owner')

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


ORM_OBJECT = Advertisement
ORM_CLS = type[Advertisement]

ORM_OBJECT_USER = User
ORM_CLS_USER = type[User]
