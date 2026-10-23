# Project Constitution

## 1. Governance & Core Principles
* **Specification-First Development (SDD)**: No implementation code or tests shall be written prior to an approved specification document utilizing Easy Approach to Requirements Syntax (EARS).
* **Test-Driven Development (TDD)**: The Red-Green-Refactor cycle is strictly enforced. Every feature or bug fix must start with a failing test before writing functional code.
* **Continuous Quality Enforcement**: All code must pass local `pre-commit` hooks and Continuous Integration (CI) checks prior to merge.

---

## 2. Technical Stack & Standards
* **Python Runtime**: Python 3.12+ managed via `uv` with standard `venv` environments.
* **Build System**: Standard PEP 517 build backend utilizing `hatchling`.
* **Data Contracts & Schemas**: `pydantic` (v2+) for all data transfer objects, settings management, and runtime schema validation.
* **Documentation**: `sphinx` with Markdown (`myst-parser`) support for auto-generated API reference and architectural guides.

---

## 3. Code Style & Quality Gates
* **PEP 8 Compliance**: Code must strictly conform to PEP 8 standards.
* **Formatting & Linting**: `ruff` is the single source of truth for code formatting, import sorting (`isort`), and linting.
* **Static Type Safety**: `mypy` running in strict mode (`strict = true`). No untyped functions or implicit `Any` types allowed.

---

## 4. Requirement Syntax (EARS)
All requirements must adhere to one of the following standard EARS templates:
* **Ubiquitous**: *The <system name> shall <system response>.*
* **Event-Driven**: *WHEN <trigger>, the <system name> shall <system response>.*
* **State-Driven**: *WHILE <in a specific state>, the <system name> shall <system response>.*
* **Unwanted Behavior**: *IF <precondition/trigger>, THEN the <system name> shall <system response>.*
* **Optional Feature**: *WHERE <feature is included>, the <system name> shall <system response>.*

---

## 5. Testing & Coverage Thresholds
* **Test Framework**: `pytest` for all unit, integration, and contract tests.
* **Coverage Engine**: `pytest-cov` enforced during local runs and CI pipelines.
* **Coverage Floor**: Minimum **95% branch coverage** required for all pull requests. Dropping total project coverage is prohibited.

---

## 6. Automation & CI Constraints
* **Pre-Commit Hooks**: Must execute `ruff check`, `ruff format --check`, `mypy`, and `pytest`.
* **CI Pipelines**: Validates all checks against multiple Python target versions on pull requests.
* **No CD Enforcement**: Deployment/release workflows are completely decoupled from CI. Merging to `main` verifies build integrity only; no auto-deployment triggers are allowed.