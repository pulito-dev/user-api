from .. import crud
from ..models import *
from .deps import get_session
from ..rabbit.client import mq_cl
from sqlmodel import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

user_router = APIRouter()

@user_router.get("/")
async def get_all_users(session: AsyncSession = Depends(get_session)) -> UsersPublic:
    
    statement = select(User)
    res = await session.execute(statement)
    users = res.scalars().all()
    
    return UsersPublic(data=users)


@user_router.get("/{id}")
async def get_user_by_id(id: int, session: AsyncSession = Depends(get_session)) -> User:

    user = await session.get(User, id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="No user found with corresponding id"
        )

    return user

@user_router.delete("/{id}")
async def delete_user(id: int, session: AsyncSession = Depends(get_session)) -> DeleteUserPublic:
    user = await session.get(User, id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"Accommdation with id {id} does not exist"
        )
    
    await crud.delete_user(session, user)

    # # send a msg to listings api to cascade delete
    # await mq_cl.send_message(
    #     "listings.cascade_delete",
    #     {
    #         "user_id": id
    #     }
    # )


    return DeleteUserPublic(msg="User deleted successfully")
