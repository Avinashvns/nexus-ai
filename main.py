from fastapi import FastAPI

from configs.settings import get_settings
from api.routes.chat import router as chat_router
from api.routes.documents import (
    router as documents_router,
)
from api.routes.workflows import (
    router as workflows_router,
)
from database.init_db import init_database

from configs.settings import get_settings
from core.config_validation import (
    validate_configuration,
)

from api.exception_handlers import (
    register_exception_handlers,
)

from api.middleware import (
    SecurityHeadersMiddleware,
)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_middleware(
    SecurityHeadersMiddleware
)

register_exception_handlers(app)

app.include_router(chat_router)

app.include_router(documents_router)

app.include_router(workflows_router)


@app.on_event("startup")
def startup_event():
    settings = get_settings()

    validate_configuration(settings)

    init_database()


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
