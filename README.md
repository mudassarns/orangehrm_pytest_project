# OrangeHRM Selenium Automation Framework

[![GitHub Actions](https://github.com/mudassarns/orangehrm_pytest_project/actions/workflows/pytest.yml/badge.svg?branch=dev)](https://github.com/mudassarns/orangehrm_pytest_project/actions/workflows/pytest.yml)

A Python test-automation portfolio demonstrating browser, REST API, database, and cross-layer testing against OrangeHRM using Selenium WebDriver and pytest.

## What this project demonstrates

- UI automation with Selenium WebDriver and reusable page objects.
- REST API validation using Python `requests`.
- MariaDB verification through parameterized database queries.
- Hybrid test workflows that combine UI, API, and database checks.
- Shared pytest fixtures for authentication, test data, and cleanup.
- Parallel execution with pytest-xdist and self-contained HTML reporting.
- CI configuration for GitHub Actions and a Buildkite pipeline definition.

## Technology stack

Python 3.14 · Selenium WebDriver · pytest · pytest-xdist · Requests · MariaDB · Docker Compose · GitHub Actions · Buildkite · pytest-html

## Test coverage

| Module | Purpose |
|---|---|
| `tests/test_ui.py` | Browser-based workflow validation |
| `tests/test_api.py` | Employee API operations and response validation |
| `tests/test_database.py` | Database-level verification of employee records |
| `tests/test_hybrid.py` | Cross-layer UI/API/database validation |

Test data is generated for test execution, and shared fixtures perform cleanup for supported employee-creation workflows.

## Project structure

```text
api/                    API client and OrangeHRM API operations
db/                     MariaDB client
pages/                  Selenium page objects
schemas/                Response schema definitions
tests/                  UI, API, database, and hybrid tests
utils/                  Browser, locator, screenshot, and test-data utilities
docker-orangehrm/       Docker Compose environment
.github/workflows/      GitHub Actions workflows
.buildkite/              Buildkite pipeline definition
config.py               Environment-based configuration
conftest.py              Shared pytest fixtures
pytest.ini              Pytest markers, logging, retries, and HTML reporting
requirements.txt        Python dependencies
.env.example             Safe template for local configuration
```

## Prerequisites

- Python 3.14
- Docker Desktop with Docker Compose
- A supported browser for Selenium execution
- Local OrangeHRM and MariaDB containers
- Credentials for the local OrangeHRM test administrator

## Local setup

Run these commands from the repository root in PowerShell.

1. Create and activate a virtual environment:

   ```powershell
   py -3.14 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies and create a private local environment file:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   Copy-Item .env.example .env
   ```

3. Edit `.env` and replace every placeholder. Keep `MARIADB_ROOT_PASSWORD`, `MARIADB_PASSWORD`, and `QA_DB_PASSWORD` consistent with the local setup. The template leaves `MARIADB_DATABASE` empty so the OrangeHRM installer can create the application database.

4. Start the containers:

   ```powershell
   docker compose --env-file .env -f docker-orangehrm/docker-compose.yml up -d --wait
   docker compose --env-file .env -f docker-orangehrm/docker-compose.yml ps
   ```

5. On a fresh database, initialize OrangeHRM before running tests. The GitHub Actions workflow's **Install OrangeHRM via official CLI installer** step documents the non-interactive installer configuration used by CI. Use your local `.env` values for the administrator and database credentials.

6. Run tests:

   ```powershell
   pytest tests/ --headless -v
   ```

## Running focused tests

```powershell
pytest tests/test_ui.py --headless -v
pytest tests/test_api.py --headless -v
pytest tests/test_database.py --headless -v
pytest tests/test_hybrid.py --headless -v
```

Run tests in parallel:

```powershell
pytest tests/ --headless -n 4 -v
```

The configured HTML report is written to `reports/test-report.html`. The `--env` option selects an environment prefix; the default is `qa`.

## Configuration and security

Copy `.env.example` to `.env` and configure these values for your local environment:

- `QA_ORANGEHRM_BASE_URL`, `QA_ORANGEHRM_USERNAME`, `QA_ORANGEHRM_PASSWORD`
- `QA_DB_HOST`, `QA_DB_PORT`, `QA_DB_NAME`, `QA_DB_USER`, `QA_DB_PASSWORD`
- MariaDB container initialization values beginning with `MARIADB_`

Never commit `.env`, real credentials, OAuth files, tokens, or test artifacts containing sensitive data. The repository's `.gitignore` excludes these local files.

## CI

- **GitHub Actions:** `.github/workflows/pytest.yml` runs on pushes to `dev` and executes the automated suite in CI.
- **Buildkite:** `.buildkite/pipeline.yml` contains a pipeline definition.

The separate `demo` branch has an additional OAuth experiment in `tests/test_oauth.py` and `.github/workflows/demo_pytest.yml`. It is not part of the default branch's core test modules. The OAuth experiment can create an employee and does not provide the same cleanup guarantee as the core fixtures; run it only against a disposable OrangeHRM environment, never a production or shared QA instance.

## Related projects

- [OrangeHRM Playwright Automation](https://github.com/mudassarns/orangehrm_playwright_project)
- [OrangeHRM AI SDET Project](https://github.com/mudassarns/orangehrm_ai_sdet_project)
