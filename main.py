from fastapi import FastAPI

from configs.settings import get_settings
from api.routes.chat import router as chat_router
from api.routes.documents import (
    router as documents_router,
)

from database.init_db import init_database

settings= get_settings()

app=FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(chat_router)

app.include_router(documents_router)

@app.on_event("startup")
def startup_event():
    init_database()

@app.get("/")
async def root():
    return {
        "message" : f"Welcome to {settings.app_name}"
    }


@app.get("/health")
async def health():
    return {
        "status" : "healthy"
    }