import bcrypt
from config import DEFAULT_ROLE,ADMIN_ROLE
from fastapi import HTTPException
from models import ORM_CLS, ORM_OBJECT, Right, Role, Token, User
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_default_role(session: AsyncSession):
    query = select(Role).where(Role.name == DEFAULT_ROLE)
    role = await session.scalar(query)
    return role


async def get_admin_role(session: AsyncSession):
    query = select(Role).where(Role.name == ADMIN_ROLE)
    role = await session.scalar(query)
    return role


async def get_role(session: AsyncSession, role_name):
    query = select(Role).where(Role.name == role_name)
    role = await session.scalar(query)
    return role


def hash_password(password: str) -> str:
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(password, hashed_password)


async def check_access_rights(
        session: AsyncSession,
        token: Token,
        model: ORM_CLS | ORM_OBJECT,
        write: bool,
        read: bool,
        owner_field: str = "user_id",
        raise_exception: bool = True,
) -> bool:
    where_args = [User.id == Token.user_id, Right.model == model._model]
    if write:
        where_args.append(Right.write == True)
    if read:
        where_args.append(Right.read == True)
    if (hasattr(model, owner_field)) and getattr(model, owner_field) != token.user_id:
        where_args.append(Right.only_own == False)

    right_query = (
        select(func.count(User.id))
        .join(Role, User.roles)
        .join(Right, Role.rights)
        .where(*where_args)
    )

    rights_count = await session.scalar(right_query)
    if not rights_count and raise_exception:
        raise HTTPException(403, detail="Access denied")
    return rights_count > 0
