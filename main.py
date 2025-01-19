from .core.db import db_cl
from fastapi import FastAPI
from .seeds import seed_rules
from .core.config import config
from .rabbit.client import mq_cl
from .auth.client import auth_cl
from contextlib import asynccontextmanager
from .rabbit.handlers.test import test_handler
from .rabbit.handlers.get_user import get_user_handler


@asynccontextmanager
async def lifespan(_: FastAPI):
    # everything before yield is executed before the app starts up
    # set up rabbit
    await mq_cl.connect(str(config.RABBIT_URI))
    await mq_cl.setup_rpc_queues()
    await mq_cl.consume("users.get_by_id.req", get_user_handler)

    # set up db
    db_cl.connect(str(config.DB_URI))
    await db_cl.create_schema(str(config.DB_SCHEMA))

    # create tables
    await db_cl.init_db()

    # seed the db
    await seed_rules()

    # setup auth client
    auth_cl.connect(
        domain=str(config.AUTH0_DOMAIN),
        client_id=str(config.AUTH0_CLIENT_ID),
        client_secret=str(config.AUTH0_CLIENT_SECRET),
    )

    yield
    
    # everything after yield is execute after the app shuts down
    await mq_cl.disconnect()
    await db_cl.disconnect()


app = FastAPI(
    title=config.TITLE,
    lifespan=lifespan
)


from .routes.auth import auth_router
from .routes.users import user_router
from .routes.roles import role_router


app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/users")
app.include_router(role_router, prefix="/roles")
