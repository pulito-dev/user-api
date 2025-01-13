import json
from sqlmodel import Session
from ...models import User, Role, UsersPublic
from ...core.db import db_cl
from aio_pika import IncomingMessage


async def get_user_handler(msg: IncomingMessage):
    # if an exception gets raised, message gets rejected and put back in the queue
    async with msg.process(requeue=True):
        print(f"REPLY TO: {msg.reply_to}")
        msg_body = json.loads(
            msg.body.decode()
        )
    
        user_id = msg_body["user_id"]

        with Session(db_cl.engine) as session:
            # TODO: join the roles
            user = await session.get(User, user_id)

        # serialize the user
        return UsersPublic.model_validate(user).model_dump_json()



