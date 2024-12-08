from .models import *
from sqlmodel import Session, select


# users
def get_user_by_nickname(session: Session, nickname: str) -> User | None:
    statement = select(User).where(User.nickname == nickname)
    user = session.exec(statement).first()

    return user


def get_user_by_idp_id(session: Session, idp_id: str) -> User | None:
    statement = select(User).where(User.idp_id == idp_id)
    user = session.exec(statement).first()

    return user


def create_user(session: Session, user_create: CreateUpdateUser) -> User:
    user = User.model_validate(
        user_create
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def delete_user(session: Session, db_user: User):
    session.delete(db_user)
    session.commit()


# roles


