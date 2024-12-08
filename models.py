from typing import Optional
from .core.config import config
from sqlmodel import Field, SQLModel


# base model for all models
# makes sure that all models are created in the appropriate schema
class BaseModel(SQLModel):
    __table_args__ = {"schema": str(config.DB_SCHEMA)}


# request models
# todo: add rule to strip and check empty strings https://stackoverflow.com/a/70262769/10513667
# todo: add a base model for inheriting common fields


# user

class CreateUpdateUser(BaseModel):
    idp_id: str
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    nickname: str
    picture: str


class User(BaseModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    idp_id: str
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    nickname: str
    picture: str


class UsersPublic(BaseModel):
    data: list[User]


class CreateUserPublic(BaseModel):
    id: int
    msg: str


class DeleteUserPublic(BaseModel):
    msg: str


# role

class CreateUpdateRole(BaseModel):
    name: str


class Role(BaseModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str


class RolesPublic(BaseModel):
    data: list[Role]


class CreateRolePublic(BaseModel):
    id: int
    msg: str


class UpdateRolePublic(BaseModel):
    user: Role
    msg: str


class DeleteRolePublic(BaseModel):
    msg: str
