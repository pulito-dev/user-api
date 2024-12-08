import secrets
from typing import Literal
from pydantic import Field, PostgresDsn, AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    model_config = SettingsConfigDict()

    # general
    ENV: Literal["dev", "test", "prod"] = Field(
        default="dev"
    )
    # fastapi
    TITLE: str = "User API"
    SECRET_KEY: str = secrets.token_urlsafe(8)

    # db
    DB_URI: PostgresDsn = Field(
        default="postgres://root:postgres@db/root"
    )
    DB_SCHEMA: str = "user"

    # rabbit
    RABBIT_URI: AmqpDsn = Field(
        default="amqp://guest:guest@mq/"
    )

config = Config()
print(config.model_dump())
