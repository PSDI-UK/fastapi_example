import sys
from enum import Enum

from pydantic import ValidationError
from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Mode(str, Enum):
    TEST = "TEST"
    DEV = "DEV"
    LIVE = "LIVE"


class Settings(BaseSettings):
    # The connection string for the MongoDB database
    mongodb_url: str = "mongodb://localhost:27017/mydatabase"

    # The level of logging.
    log_level: LogLevel = LogLevel.DEBUG

    # The mode (TEST, DEV, LIVE) the application is running in
    mode: Mode = Mode.DEV

    # The origins that are allowed to make requests. This needs to be set when used in conjunction
    # with a web app.
    allow_origins: str = "http://localhost"

    class Config:
        env_file = ".env"

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as e:  # pragma: no cover
            print(f"Invalid configuration: {e}")
            sys.exit(1)


settings = Settings()
