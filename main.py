from .core.db import db_cl
from fastapi import FastAPI
from .core.config import config
from .rabbit.client import mq_cl
from contextlib import asynccontextmanager
from sqlalchemy.schema import CreateSchema
from .rabbit.handlers.test import test_handler


@asynccontextmanager
async def lifespan(_: FastAPI):
    # everything before yield is executed before the app starts up
    # set up rabbit
    await mq_cl.connect(str(config.RABBIT_URI))
    await mq_cl.consume("users", test_handler)

    # set up db
    db_cl.connect(str(config.DB_URI))
    with db_cl.engine.connect() as conn:
        conn.execute(CreateSchema(str(config.DB_SCHEMA), if_not_exists=True))
        conn.commit()
    
    # create tables
    db_cl.init_db()

    yield
    
    # everything after yield is execute after the app shuts down
    await mq_cl.disconnect()
    db_cl.disconnect()


app = FastAPI(
    title=config.TITLE,
    lifespan=lifespan
)


from .routes.auth import auth_router
from .routes.users import user_router
# from .routes.roles import role_router


app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/users")
# app.include_router(role_router, prefix="/roles")
