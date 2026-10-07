"""Tests for generated API models (regenerate via codegen.ps1 / codegen.sh)."""

import pytest
from pydantic import ValidationError

from driven_dev.api_models import Health, Status


def test_health_validates_and_round_trips() -> None:
    health = Health.model_validate({"status": "ok", "version": "0.1.0"})
    assert health.status is Status.ok
    assert Health.model_validate_json(health.model_dump_json()) == health


def test_health_rejects_unknown_status() -> None:
    with pytest.raises(ValidationError):
        Health.model_validate({"status": "on-fire", "version": "0.1.0"})


def test_health_requires_version() -> None:
    with pytest.raises(ValidationError):
        Health.model_validate({"status": "degraded"})
