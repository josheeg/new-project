"""driven-dev package."""

from driven_dev.settings import get_settings


def main() -> None:
    """Print a greeting using the configured app name."""
    print(f"Hello from {get_settings().app_name}!")
