from .. import crud
from ..models import *
from sqlmodel import select
from ..rabbit.client import mq_cl
from .deps import get_session, get_current_user
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Header

user_router = APIRouter()

@user_router.get("/")
async def get_all_users(session: AsyncSession = Depends(get_session)) -> UsersPublic:
    
    statement = select(User)
    res = await session.execute(statement)
    users = res.scalars().all()
    
    return UsersPublic(data=users)

@user_router.get("/me")
async def get_me(session: AsyncSession = Depends(get_session), x_forwarded_user: int = Header()) -> User:
    user = await session.get(User, x_forwarded_user)

    return user


@user_router.get("/{idp_id}")
async def get_user_by_idp_id(idp_id: str, session = Depends(get_session)):
    user = await crud.get_user_by_idp_id(session, idp_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="No user found with corresponding id"
        )

    return user


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
async def delete_user(id: int, session: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)) -> DeleteUserPublic:
    user = await session.get(User, id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {id} does not exist"
        )
    
    if user.id != current_user.get("id"):
        print("403")
        raise HTTPException(
            status_code=403,
            detail="You can't delete this profile"
        )
    
    session.begin()
    try:
        await crud.delete_user(session, user)

        # send a msg to accommodations api to cascade delete
        res = await mq_cl.send_rpc_message(
            "accommodations.cascade_delete",
            {
                "user_id": id
            }
        )

        if not res.get("success"):
            raise Exception()
    except:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=res.get("msg", "Something went wrong")
        )
    else:
        await session.commit()
        return DeleteUserPublic(msg="User deleted successfully")
