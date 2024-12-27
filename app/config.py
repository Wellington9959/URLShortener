import os

from pydantic_settings import BaseSettings
from starlette.config import Config

current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", ".env")
config = Config(env_path)


class AppSettings(BaseSettings):
    APP_NAME: str = config("APP_NAME", default="URL Shortening Service")
    APP_SUMMARY: str = config(
        "APP_SUMMARY",
        default="""
        The API provides endpoints to create, retrieve, update, and delete short URLs.
        It also provides statistics on the number of times a short URL has been accessed.
        """,  # noqa: E501
    )
    TESTING: bool = config("TESTING", default=False)
    DEBUG: bool = config("DEBUG", default=False)


class LoggerSettings(BaseSettings):
    LOGGING_LEVEL: str | None = config("LOGGING_LEVEL", default="INFO")


class DatabaseSettings(BaseSettings):
    MONGO_URI: str = config("MONGO_URI")


class Settings(AppSettings, LoggerSettings, DatabaseSettings):
    pass


settings = Settings()
