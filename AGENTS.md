# AGENTS.md

## Project

End-to-end UI tests for an external LMS application. The stack is Python 3.11, pytest, synchronous Playwright, Pydantic Settings, Allure, and `ui-coverage-tool`.

Main directories:

- `tests/` — test scenarios grouped by product area.
- `pages/` — page objects coordinating page-level behavior.
- `components/` — reusable UI regions and workflows.
- `elements/` — low-level Playwright wrappers with logging, Allure, and UI coverage.
- `fixtures/` — browser lifecycle, authenticated state, page objects, and reporting.
- `tools/` — routes and Playwright/Allure helpers.
- `scripts/` — examples and debugging utilities, not the primary test suite.

## Setup

Use Python 3.11 to match CI:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install
```

Configuration is loaded from `.env` by `config.py`. Preserve its Pydantic nested-key syntax and never expose or replace credentials. Important settings include `APP_URL`, `HEADLESS`, `BROWSERS`, `TEST_USER.*`, `TEST_DATA.IMAGE_PNG_FILE`, and `UI_COVERAGE_*`.

## Running tests

`pytest.ini` enables verbose output, Allure results, and automatic xdist parallelism.

```bash
# A single test, serialized for debugging
pytest tests/dashboard/test_dashboard.py::TestDashboard::test_dashboard_displaying -n 0

# A product area
pytest tests/courses -m courses -n 0

# Regression suite with CI concurrency
pytest -m regression --numprocesses 2

# Full configured suite
pytest
```

Use only registered markers from `pytest.ini`; register new markers there. Tests use an external, stateful LMS and share `TEST_USER`, so avoid assumptions about execution order or pristine server state. Diagnose state-related failures with an exact `-n 0` rerun first.

Test runs generate `allure-results/`, `tracing/`, `videos/`, and `browser-state.json`. Do not edit or commit these artifacts unless explicitly requested. Use `ui-coverage-tool save-report` only when a coverage report is required.

## Implementation conventions

Follow the existing dependency flow:

```text
pytest test -> page object -> component -> element wrapper -> Playwright locator
```

- Keep tests declarative; selectors and repeated UI operations belong in lower layers.
- Use `playwright.sync_api` only. Prefer Playwright's web-first `expect(...)` assertions and never add fixed sleeps.
- Select controls by `data-testid`. `BaseElement` accepts the test-id value, not arbitrary CSS or XPath.
- Prefer wrappers from `elements/` over raw locators so logging, Allure steps, and UI coverage remain consistent.
- Use the existing `str.format(**kwargs)` and `nth` conventions for collections and parameterized test ids.
- Create components for reusable UI regions and page objects for behavior coordinating multiple components.
- Initialize child objects in `__init__`, pass the same Playwright `Page`, and call the parent constructor.
- Give actions domain-oriented names; do not leak locator mechanics into tests.
- Wrap composite component actions and checks in `@allure.step`. Element methods already create their own steps.
- New element actions/assertions must call `track_coverage` with the matching `ActionType` after success.
- Navigate with `AppRoute` and `BasePage.visit()` rather than duplicating URLs.
- Add page-object fixtures to `fixtures/pages.py`. Use `page` for anonymous flows and `page_with_state` for authenticated flows.
- Reuse the session storage state instead of logging in separately in each authenticated test.

## Test metadata

Follow the established test structure: class-level pytest markers and Allure hierarchy, plus `@allure.title` and severity for each test. Extend enums in `tools/allure/` for new product areas instead of scattering string literals.

Name files `test_*.py`, classes `Test*`, and functions `test_*`. Keep browser teardown intact: each test context records trace and video and attaches them to Allure.

Static images, fonts, and media are normally aborted in `mock_static_resources()`. If a scenario must verify one of them, add a narrow exception rather than disabling the optimization globally.

## Verification and handoff

Run at least the directly affected test. Do not weaken assertions to hide flakiness; check locator ownership, application state, and waiting behavior first. If the LMS or browser is unavailable, report the test as unverified. In the final handoff, list the checks performed and any environment-specific behavior not covered.
