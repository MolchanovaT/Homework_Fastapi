import datetime
import uuid

from config import PG_DSN
from data_types import ModelName
from sqlalchemy import (UUID, Boolean, CheckConstraint, Column, DateTime,
                        ForeignKey, Integer, Float, String, Table, UniqueConstraint,
                        func)
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, WriteOnlyMapped, mapped_column, relationship

engine = create_async_engine(
    PG_DSN,
)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


role_rights = Table(
    "role_rights_relation",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), index=True),
    Column("right_id", ForeignKey("right.id"), index=True),
)
user_roles = Table(
    "user_roles_relation",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), index=True),
    Column("role_id", ForeignKey("role.id"), index=True),
)


class Right(Base):
    __tablename__ = "right"
    _model = "Right"
    id: Mapped[int] = mapped_column(primary_key=True)
    write: Mapped[bool] = mapped_column(Boolean, default=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    only_own: Mapped[bool] = mapped_column(Boolean, default=False)
    model: Mapped[ModelName] = mapped_column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("model", "only_own", "read", "write"),
        CheckConstraint("model in ('User', 'Advertisement', 'Role', 'Right')"),
    )


class Role(Base):
    __tablename__ = "role"
    _model = "Role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    rights: Mapped[list[Right]] = relationship(secondary=role_rights, lazy="joined")


class Advertisement(Base):
    __tablename__ = "advertisements"
    _model = "Advertisement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    price: Mapped[float] = mapped_column(Float, default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    user: Mapped["User"] = relationship("User", lazy="joined", back_populates="advertisements")

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "price": self.price,
            "user_id": self.user_id,
        }


class User(Base):
    __tablename__ = "users"
    _model = "User"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(72), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    tokens: Mapped[list["Token"]] = relationship(
        "Token", lazy="joined", back_populates="user"
    )
    advertisements: WriteOnlyMapped['Advertisement'] = relationship('Advertisement', lazy="joined",
                                                                    back_populates='user')
    roles: Mapped[list["Role"]] = relationship(
        Role, secondary=user_roles, lazy="joined"
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Token(Base):
    __tablename__ = "token"
    _model = "Token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        UUID,
        server_default=func.gen_random_uuid(),
        unique=True,
    )
    creation_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship("User", lazy="joined", back_populates="tokens")

    @property
    def dict(self):
        return {
            "id": self.id,
            "token": str(self.token),
            "user_id": self.user_id,
            "creation_time": self.creation_time.isoformat(),
        }


ORM_OBJECT = Advertisement | User | Token
ORM_CLS = type[Advertisement] | type[User] | type[Token]
