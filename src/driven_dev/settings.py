"""Application settings loaded from the environment via pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven settings.

    Env vars use the ``DRIVEN_DEV_`` prefix (e.g. ``DRIVEN_DEV_APP_NAME``);
    a repo-root ``.env`` is read if present (never committed).
    """

    model_config = SettingsConfigDict(
        env_prefix="DRIVEN_DEV_", env_file=".env", extra="ignore"
    )

    app_name: str = "driven-dev"
    debug: bool = False
    log_level: str = "INFO"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings; tests clear it via ``get_settings.cache_clear()``."""
    return Settings()
