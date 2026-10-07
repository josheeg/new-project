"""Render documentation diagrams with the ``diagrams`` package.

Usage::

    uv run python render_diagrams.py

Regenerates the committed PNGs in ``docs/assets/``. Requires graphviz
(``dot``) on PATH — installed via ``winget install Graphviz.Graphviz``.
Deliberately NOT part of the check chain: rendering is a manual, infrequent
step and the outputs are committed.
"""

from pathlib import Path

from diagrams import Diagram, Edge, Node

ASSETS = Path(__file__).resolve().parent / "docs" / "assets"

VERIFY_CHAIN = [
    "ruff check",
    "ruff format --check",
    "mypy (strict)",
    "import-linter",
    "spec contract (codegen -Check)",
    "interrogate (100%)",
    "docs build (strict)",
    "pytest (cov >= 90%)",
]


def render_verify_chain() -> None:
    """Render the fail-fast verification chain to ``docs/assets/verify-chain.png``."""
    ASSETS.mkdir(exist_ok=True)
    with Diagram(
        "Verification chain (fail-fast, stops at first failure)",
        show=False,
        outformat="png",
        filename=str(ASSETS / "verify-chain"),
        direction="LR",
        # Let boxes grow with their labels instead of clipping at 1.4in.
        node_attr={"fixedsize": "false"},
    ):
        previous: Node | None = None
        for gate in VERIFY_CHAIN:
            current = Node(gate)
            if previous is not None:
                previous >> Edge(label="pass") >> current
            previous = current


if __name__ == "__main__":
    render_verify_chain()
