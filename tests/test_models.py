"""Tests for hand-written domain models."""

from datetime import UTC
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from driven_dev.models import Task, TaskStatus


def test_task_defaults() -> None:
    task = Task(title="Write docs")
    assert task.status is TaskStatus.PENDING
    assert task.tags == []
    assert isinstance(task.id, UUID)
    assert task.created_at.tzinfo is UTC


def test_task_strips_title_and_normalizes_tags() -> None:
    task = Task(title="  Ship it  ", tags=[" a ", "a", " ", "b"])
    assert task.title == "Ship it"
    assert task.tags == ["a", "b"]


def test_task_rejects_blank_title() -> None:
    with pytest.raises(ValidationError, match="title must not be blank"):
        Task(title="   ")


def test_task_json_round_trip() -> None:
    task = Task(id=uuid4(), title="Round trip", status=TaskStatus.DONE, tags=["x"])
    assert Task.model_validate_json(task.model_dump_json()) == task
