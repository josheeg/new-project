"""Spec-first API: connexion serves routes from ``openapi/openapi.yaml``.

Handlers are wired via ``operationId`` + ``x-openapi-router-controller`` in
the spec — adding an operation means adding the spec entry first, then the
function here.
"""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from connexion import FlaskApp

try:
    APP_VERSION = version("driven-dev")
except PackageNotFoundError:  # pragma: no cover - only when package metadata is absent
    APP_VERSION = "0.0.0"

# Repo-root openapi/ dir (editable install: src/driven_dev/api.py -> parents[2]).
SPEC_DIR = Path(__file__).resolve().parents[2] / "openapi"


def get_health() -> dict[str, str]:
    """GET /health — response is validated against the Health schema."""
    return {"status": "ok", "version": APP_VERSION}


def create_app() -> FlaskApp:
    """Build the connexion app with strict request/response validation."""
    app = FlaskApp(__name__, specification_dir=str(SPEC_DIR))
    app.add_api(
        "openapi.yaml",
        strict_validation=True,
        validate_responses=True,
    )
    return app


if __name__ == "__main__":
    create_app().run(port=8080)
