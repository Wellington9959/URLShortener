from typing import Any

from fastapi import APIRouter, FastAPI

from app.config import (
    AppSettings,
    DatabaseSettings,
    LoggerSettings,
)
from app.utilities.logger_middleware import process_time_log_middleware


def add_process_time_log_middleware(app: FastAPI):
    app.middleware("http")(process_time_log_middleware)


def create_application(
    router: APIRouter,
    settings: (AppSettings | DatabaseSettings | LoggerSettings),
    **kwargs: Any,
) -> FastAPI:
    # Before creating application
    if isinstance(settings, AppSettings):
        to_update = {
            "title": settings.APP_NAME,
            "summary": settings.APP_SUMMARY,
        }
        kwargs.update(to_update)

    application = FastAPI(**kwargs)
    application.include_router(router)

    add_process_time_log_middleware(application)

    return application
