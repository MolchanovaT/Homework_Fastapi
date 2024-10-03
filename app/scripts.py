import asyncio

from models import Right, Role, Session, Advertisement, User
from sqlalchemy.ext.asyncio import AsyncSession


async def create_default_role(session: AsyncSession):
    rights = []

    for wr in True, False:
        for model in Advertisement, User:
            right = Right(model=model._model, only_own=True, read=wr, write=not wr)
            rights.append(right)
    role = Role(name="user", rights=rights)
    session.add_all([role, *rights])
    await session.commit()


async def create_admin_role(session: AsyncSession):
    rights = []

    for model in Advertisement, User:
        right = Right(model=model._model, only_own=False, read=True, write=True)
        rights.append(right)
    role = Role(name="admin", rights=rights)
    session.add_all([role, *rights])
    await session.commit()


async def main():
    async with Session() as session:
        await create_default_role(session)
        await create_admin_role(session)


if __name__ == "__main__":
    asyncio.run(main())
