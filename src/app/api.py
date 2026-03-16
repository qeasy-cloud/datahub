from datetime import datetime, timezone

from fastapi import APIRouter

from app.config import get_settings
from app.schemas import HealthResponse, ProjectResponse

router = APIRouter()


@router.get("/health", tags=["system"], response_model=HealthResponse)
def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/project", tags=["project"], response_model=ProjectResponse)
def project_info() -> ProjectResponse:
    settings = get_settings()
    return ProjectResponse(
        name=settings.app_name,
        company=settings.company_name,
        website=settings.website,
        version=settings.app_version,
        api_prefix=settings.api_prefix,
        features=[
            "项目欢迎页",
            "健康检查接口",
            "项目元信息接口",
            "Swagger / ReDoc 文档",
        ],
    )
