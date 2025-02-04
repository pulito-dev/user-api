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

    # auth0 credentials
    AUTH0_DOMAIN: str = Field(
        default="pulito.eu.auth0.com"
    )
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_JWKS_URL: str | None = Field(default=None)
    AUTH0_MGMT_API_URL: str | None = Field(default=None)


config = Config()
print(config.model_dump())
