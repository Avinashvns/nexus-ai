from fastapi import FastAPI

from configs.settings import get_settings

settings= get_settings()

app=FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

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