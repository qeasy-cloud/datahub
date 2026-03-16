from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class WelcomeResponse(BaseModel):
    name: str
    description: str
    company: str
    website: str
    docs_url: str
    redoc_url: str
    openapi_url: str
    health_url: str


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str
    timestamp: datetime


class ProjectResponse(BaseModel):
    name: str
    company: str
    website: str
    version: str
    api_prefix: str
    features: list[str]
