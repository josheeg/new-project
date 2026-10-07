"""Tests for environment-driven settings."""

from collections.abc import Iterator

import pytest

from driven_dev.settings import get_settings


@pytest.fixture(autouse=True)
def _clear_settings_cache() -> Iterator[None]:
    """Settings are cached module-wide; reset around every test."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_defaults() -> None:
    settings = get_settings()
    assert settings.app_name == "driven-dev"
    assert settings.debug is False
    assert settings.log_level == "INFO"


def test_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DRIVEN_DEV_APP_NAME", "custom-app")
    assert get_settings().app_name == "custom-app"
