from .. import crud
from ..models import *
from .deps import get_db
from ..rabbit.client import mq_cl
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException

user_router = APIRouter()

@user_router.get("/")
async def get_all_users(session: Session = Depends(get_db)) -> UsersPublic:
    
    statement = select(User)
    users = session.exec(statement).all()
    
    return UsersPublic(data=users)


@user_router.get("/{id}")
async def get_user_by_id(id: int, session: Session = Depends(get_db)) -> User:

    user = session.get(User, id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="No user found with corresponding id"
        )

    return user

@user_router.delete("/{id}")
async def delete_user(id: int, session: Session = Depends(get_db)) -> DeleteUserPublic:
    user = session.get(User, id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"Accommdation with id {id} does not exist"
        )
    
    crud.delete_user(session, user)

    # # send a msg to listings api to cascade delete
    # await mq_cl.send_message(
    #     "listings.cascade_delete",
    #     {
    #         "user_id": id
    #     }
    # )


    return DeleteUserPublic(msg="User deleted successfully")
