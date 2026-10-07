"""Smoke tests for the driven_dev CLI entrypoint."""

import pytest

from driven_dev import main


def test_main_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    """The entrypoint prints the greeting line."""
    main()
    assert capsys.readouterr().out == "Hello from driven-dev!\n"
