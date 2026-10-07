"""Hand-written domain models — the canonical layer.

API DTOs are generated into ``driven_dev.api_models``; convert at the boundary,
don't edit generated code or duplicate its shapes here.
"""

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class TaskStatus(StrEnum):
    """Lifecycle states for a task."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(BaseModel):
    """A unit of work tracked by driven-dev."""

    id: UUID = Field(default_factory=uuid4)
    title: str = Field(min_length=1, max_length=120)
    status: TaskStatus = TaskStatus.PENDING
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        """Strip the title and reject whitespace-only input."""
        stripped = value.strip()
        if not stripped:
            msg = "title must not be blank"
            raise ValueError(msg)
        return stripped

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, value: list[str]) -> list[str]:
        """Strip tags, drop empties, de-duplicate while preserving order."""
        return list(dict.fromkeys(tag.strip() for tag in value if tag.strip()))
