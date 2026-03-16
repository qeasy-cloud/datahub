from fastapi import FastAPI

from app.api import router as api_router
from app.config import get_settings
from app.schemas import WelcomeResponse


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        contact={
            "name": settings.company_name,
            "url": settings.website,
        },
    )

    @application.get("/", tags=["meta"], response_model=WelcomeResponse)
    def read_root() -> WelcomeResponse:
        return WelcomeResponse(
            name=settings.app_name,
            description=settings.app_description,
            company=settings.company_name,
            website=settings.website,
            docs_url="/docs",
            redoc_url="/redoc",
            openapi_url="/openapi.json",
            health_url=f"{settings.api_prefix}/health",
        )

    application.include_router(api_router, prefix=settings.api_prefix)
    return application


app = create_app()
