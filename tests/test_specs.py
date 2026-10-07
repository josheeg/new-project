"""Executable specifications: Gherkin features wired into pytest via pytest-bdd.

Feature files live in ``tests/features/``. Scenarios carry the ``@spec`` tag
(inherited from their feature), which pytest-bdd converts into the registered
``spec`` marker — so ``uv run pytest -m spec`` selects the spec suite and
``--strict-markers`` keeps unknown tags out.
"""

import re
from typing import cast

import pytest
from httpx2 import Response
from pydantic import ValidationError
from pytest_bdd import given, parsers, scenarios, then, when
from starlette.testclient import TestClient

from driven_dev.api import create_app
from driven_dev.models import Task

scenarios("features")

_TAG_LIST = r'(?P<tags>(?:"[^"]*"\s*,\s*)*"[^"]*")'


@pytest.fixture()
def client() -> TestClient:
    """In-process connexion app client shared by API scenarios."""
    return cast(TestClient, create_app().test_client())


@when(parsers.parse('I request "{path}"'), target_fixture="api_response")
def request_path(client: TestClient, path: str) -> Response:
    """GET ``path`` on the in-process app."""
    return client.get(path)


@then(parsers.parse("the response status is {code:d}"))
def response_status(api_response: Response, code: int) -> None:
    """The HTTP status code equals ``code``."""
    assert api_response.status_code == code


@then(parsers.parse('the response body field "{field}" is "{value}"'))
def body_field(api_response: Response, field: str, value: str) -> None:
    """The JSON body field ``field`` equals ``value``."""
    assert api_response.json()[field] == value


@then(parsers.parse('the response body has field "{field}"'))
def body_has_field(api_response: Response, field: str) -> None:
    """The JSON body contains ``field``."""
    assert field in api_response.json()


@given(
    parsers.re(r'a task titled "(?P<title>[^"]*)" with tags ' + _TAG_LIST),
    target_fixture="task",
)
def task_with_tags(title: str, tags: str) -> Task:
    """A Task constructed with raw tags — validators run at construction."""
    return Task(title=title, tags=re.findall(r'"([^"]*)"', tags))


@then(parsers.re(r"the task tags are " + _TAG_LIST))
def task_tags(task: Task, tags: str) -> None:
    """The task's normalized tags equal the quoted list, in order."""
    assert task.tags == re.findall(r'"([^"]*)"', tags)


@when(
    parsers.parse('I create a task titled "{title}"'),
    target_fixture="creation_error",
)
def create_task(title: str) -> str | None:
    """Attempt task construction; capture the validation error message."""
    try:
        Task(title=title)
    except ValidationError as exc:
        return str(exc.errors()[0]["msg"])
    return None


@then(parsers.parse('task creation fails with "{message}"'))
def creation_fails(creation_error: str | None, message: str) -> None:
    """Construction raised a validation error containing ``message``."""
    assert creation_error is not None
    assert message in creation_error
