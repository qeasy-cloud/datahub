from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app import __version__


class Settings(BaseSettings):
    app_name: str = "QEasy DataHub API"
    app_description: str = "QEasy DataHub open-source starter service"
    app_version: str = __version__
    api_prefix: str = "/api/v1"
    debug: bool = False
    website: str = "https://www.qeasy.cloud/"
    company_name: str = "广东轻亿云软件科技有限公司"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
