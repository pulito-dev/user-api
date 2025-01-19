import json
from ..client import mq_cl
from sqlmodel import select
from ...models import User, Role
from aio_pika import IncomingMessage
from sqlalchemy.orm import joinedload
from ...routes.deps import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession


async def get_user_handler(msg: IncomingMessage):
    # if an exception gets raised, message gets rejected and put back in the queue
    async with msg.process(requeue=True):
        msg_body = json.loads(
            msg.body.decode()
        )
    
        user_id = msg_body["user_id"]

        session_gen = get_session()
        session: AsyncSession = await anext(session_gen)

        statement = select(User, Role).where(User.id == user_id).join(Role).options(joinedload(User.role, innerjoin=True))
        user: User = await session.scalar(statement)

        # serialize the user and inject role object into user
        # because sqlalchemy is doing some delayed query bullshit
        if user is not None:
            role = user.role
            user = user.model_dump(exclude={"role_id"})
            user["role"] = role.model_dump()

        # return user
        await mq_cl.send_rpc_response("users.get_by_id",
            { "data": user },
            msg.correlation_id
        )

    