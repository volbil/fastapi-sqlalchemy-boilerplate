from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import sessionmanager
import fastapi.openapi.utils as fu
from .settings import get_settings
from fastapi import FastAPI
from . import errors


def create_app(init_db: bool = True) -> FastAPI:
    settings = get_settings()
    lifespan = None

    # SQLAlchemy initialization process
    if init_db:
        sessionmanager.init(settings.database.endpoint)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    fu.validation_error_response_definition = (
        errors.ErrorResponse.model_json_schema()
    )

    app = FastAPI(
        title="API Docs",
        version="0.1.0",
        openapi_tags=[
            {"name": "Auth"},
            {"name": "User"},
        ],
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(errors.Abort, errors.abort_handler)
    app.add_exception_handler(
        RequestValidationError,
        errors.validation_handler,
    )

    from .permission import router as permission_router
    from .user import router as user_router
    from .auth import router as auth_router

    app.include_router(permission_router)
    app.include_router(user_router)
    app.include_router(auth_router)

    @app.get("/ping")
    async def ping_pong():
        return "pong"

    return app
