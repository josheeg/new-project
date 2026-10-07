"""Property-based contract tests generated from the OpenAPI spec.

The schema is loaded THROUGH the app (connexion serves /openapi.yaml), so
requests are dispatched in-process against the real routes.
"""

from typing import Any

from schemathesis import Case
from schemathesis.openapi import from_asgi
from schemathesis.pytest import parametrize
from schemathesis.schemas import APIOperation

from driven_dev.api import create_app

API_SCHEMA = from_asgi("/openapi.yaml", create_app())


@parametrize(api=API_SCHEMA)
def test_api_contract(case: Case[APIOperation[Any, Any, Any, Any]]) -> None:
    """Every generated request conforms to the spec; responses validate too."""
    case.call_and_validate()
