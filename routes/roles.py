from .. import crud
from ..models import *
from .deps import get_db
from ..rabbit.client import mq_cl
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException


role_router = APIRouter()


@role_router.get("/")
async def get_all_roles(session: Session = Depends(get_db)) -> RolesPublic:
    
    statement = select(Role)
    roles = session.exec(statement).all()
    
    return RolesPublic(data=roles)


@role_router.get("/{id}")
async def get_role_by_id(id: int, session: Session = Depends(get_db)) -> Role:

    role = session.get(Role, id)

    if not role:
        raise HTTPException(
            status_code=404,
            detail="No role found with corresponding id"
        )

    return role


@role_router.post("/", status_code=201)
async def create_role(create_role: CreateUpdateRole, session: Session = Depends(get_db)) -> CreateRolePublic:
    existing_role = crud.get_role_by_name(session, create_role.name.strip())

    if existing_role:
        raise HTTPException(
            status_code=400,
            detail=f"Accommdation with name {create_role.name} already exists"
        )
    
    role = crud.create_role(session, create_role)

    return CreateRolePublic(
        id=role.id,
        msg="Role created successfully"
    )


@role_router.patch("/{id}")
async def update_role(id: int, update_role: CreateUpdateRole, session: Session = Depends(get_db)) -> UpdateRolePublic:
    role = session.get(Role, id)

    # if id is invalid, return 404
    if not role:
        raise HTTPException(
            status_code=404,
            detail=f"Accommdation with id {id} does not exist"
        )
    
    existing_role = crud.get_role_by_name(session, update_role.name.strip())

    # if name is duplicate, return 400
    # check if role is being updated with same data; if yes, proceed and if no, return 400
    if existing_role and existing_role.id != id:
        raise HTTPException(
            status_code=400,
            detail=f"Accommdation with name {update_role.name} already exists"
        )
    
    role = crud.update_role(session, role, update_role)

    return UpdateRolePublic(role=role, msg=f"Role {role.name} updated successfully")
    

@role_router.delete("/{id}")
async def delete_role(id: int, session: Session = Depends(get_db)) -> DeleteRolePublic:
    role = session.get(Role, id)

    if not role:
        raise HTTPException(
            status_code=404,
            detail=f"Accommdation with id {id} does not exist"
        )
    
    crud.delete_role(session, role)

    # send a msg to listings api to cascade delete
    await mq_cl.send_message(
        "listings.cascade_delete",
        {
            "role_id": id
        }
    )


    return DeleteRolePublic(msg="Role deleted successfully")
