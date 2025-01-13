from .models import *
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession


# users
def get_user_by_nickname(session: AsyncSession, nickname: str) -> User | None:
    statement = select(User).where(User.nickname == nickname)
    user = session.exec(statement).first()

    return user


async def get_user_by_idp_id(session: AsyncSession, idp_id: str) -> User | None:
    statement = select(User).where(User.idp_id == idp_id)
    res = await session.execute(statement)

    user = res.scalars().first()

    return user


async def create_user(session: AsyncSession, user_create: CreateUpdateUser) -> User:
    user = User.model_validate(
        user_create
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def delete_user(session: AsyncSession, db_user: User):
    await session.delete(db_user)
    await session.commit()


# roles
async def create_role(session: AsyncSession, role_create: CreateUpdateRole):
    role = Role.model_validate(
        role_create
    )

    session.add(role)
    await session.commit()
    await session.refresh(role)

    return role

async def delete_role(session: AsyncSession, db_role: Role):
    await session.delete(db_role)
    await session.commit()
