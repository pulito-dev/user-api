from .models import *
from sqlmodel import select
from .routes.deps import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession

async def seed_rules():
    # get sesion by using async generator
    session_gen = get_session()
    session: AsyncSession = await anext(session_gen)

    # check if roles already exist
    statement = select(Role)
    res = await session.execute(statement)
    roles_exist = res.scalar()

    if roles_exist:
        print("roles exist already, skipping seeding roles")
        return

    regular_role = Role(
        name="REGULAR"
    )
    admin_role = Role(
        name="ADMIN"
    )

    roles = [
        regular_role,
        admin_role
    ]

    session.add_all(roles)
    await session.commit()