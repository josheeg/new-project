"""Property-based tests (hypothesis) for model invariants."""

from hypothesis import given, settings
from hypothesis import strategies as st

from driven_dev.models import Task, TaskStatus


@given(st.lists(st.text()))
@settings(deadline=1000)
def test_tag_normalization_invariants(tags: list[str]) -> None:
    """Tags come out stripped, non-empty, de-duplicated; membership preserved."""
    task = Task(title="x", tags=tags)
    assert all(tag.strip() == tag and tag != "" for tag in task.tags)
    assert len(task.tags) == len(set(task.tags))
    assert set(task.tags) == {t.strip() for t in tags if t.strip()}


@given(
    title=st.text(min_size=1, max_size=120).filter(lambda s: s.strip() != ""),
    status=st.sampled_from(TaskStatus),
    tags=st.lists(st.text()),
)
@settings(deadline=1000)
def test_task_json_round_trip(title: str, status: TaskStatus, tags: list[str]) -> None:
    """Any valid Task survives a JSON round trip unchanged."""
    task = Task(title=title, status=status, tags=tags)
    assert Task.model_validate_json(task.model_dump_json()) == task
