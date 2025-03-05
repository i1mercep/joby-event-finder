from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"case_sensitive": False, "env_file_encoding": "utf-8"}
    app_name: str = "Event Finder API"
    log_level: str = "INFO"
    database_url: str
    api_prefix: str = "/api/v1"
    admin_username: str | None = None
    admin_email: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
