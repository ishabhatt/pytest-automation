# Pytest Automation Framework

UI automation framework built with `pytest`, `selenium`, and the Page Object Model. 
The project targets the SauceDemo application and demonstrates environment-driven execution, 
centralized test reporting, and CI quality gates.

## Stack

- Python
- Pytest
- Selenium WebDriver
- Page Object Model
- Allure Report
- pytest-html
- Ruff
- pre-commit
- GitHub Actions

## Framework Features

- Page Object Model structure under `pages/`
- Cross-browser execution for Chrome, Firefox, and Edge
- Headless execution support with `--headless`
- Environment selection with `--env`
- Data-driven test coverage using CSV test data
- HTML report generation with `pytest-html`
- Allure result generation with screenshot and page-source capture on failure
- Ruff-based linting and formatting
- Pre-commit hooks for local quality checks
- GitHub Actions workflows for PR quality checks and post-merge test execution

## Project Structure

```text
pytest-automation/
├── config/
│   └── config.ini
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── navigation_page.py
│   └── products_page.py
├── testdata/
│   └── login_data.csv
├── tests/
│   ├── conftest.py
│   ├── test_login.py
│   ├── test_login_datadriven.py
│   └── test_login_error.py
├── .github/workflows/
├── pyproject.toml
├── pytest.ini
└── .pre-commit-config.yaml
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd pytest-automation
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install .
```

## Running Tests

### Smoke suite

```bash
pytest -m smoke --browser chrome --headless --alluredir=allure-results
```

### Regression suite

```bash
pytest -m regression --browser chrome --headless --alluredir=allure-results
```

### Run against a specific environment

```bash
pytest -m smoke --browser chrome --env qa --headless --alluredir=allure-results
```

### Supported CLI options

- `--browser`: `chrome`, `firefox`, `edge`
- `--env`: `dev`, `qa`, `stage`, `prod`
- `--headless`: runs browser without UI

## Adding New Tests

Create new tests under `tests/` and reuse page objects from `pages/`.

### Example test skeleton

```python
import logging
import pytest
import allure

from pages.login_page import LoginPage


class TestExample:
    logger = logging.getLogger()

    @allure.epic("Login")
    @allure.feature("Authentication")
    @allure.story("Example test")
    @pytest.mark.smoke
    def test_example(self, setup, env_config):
        driver = setup

        with allure.step("Open application"):
            driver.get(env_config["baseURL"])

        login_page = LoginPage(driver)

        with allure.step("Perform action"):
            login_page.enter_username(env_config["username"])
            login_page.enter_password(env_config["password"])
            login_page.submit()
```

### Recommended pattern

- Add locators and reusable actions in a page object under `pages/`
- Keep test logic inside `tests/`
- Use `env_config` for environment-specific values
- Use `allure.step(...)` for readable reporting
- Mark tests with `@pytest.mark.smoke` or `@pytest.mark.regression`
- Use direct assertions with clear failure messages

### If test data is needed

Store test data under `testdata/` and load it through `utils/data_reader.py`.

### If a new page is needed

Create a new page class under `pages/` and inherit from `BasePage` so common actions like `find_element`, `click`, and wait helpers are reused.

## Reports

### pytest-html

HTML reports are generated automatically under `reports/`.

### Allure

Generate test results:

```bash
pytest -m smoke --browser chrome --headless --alluredir=allure-results
```

Serve the Allure report:

```bash
allure serve allure-results
```

Or generate static report files:

```bash
allure generate allure-results -o allure-report --clean
```

## Code Quality

### Ruff

Lint:

```bash
ruff check .
```

Format check:

```bash
ruff format --check .
```

Auto-fix and format:

```bash
ruff check . --fix
ruff format .
```

### pre-commit

Install hooks:

```bash
pre-commit install
```

Run all hooks manually:

```bash
pre-commit run --all-files
```

## CI

The repository includes two GitHub Actions workflows:

- `pr-quality.yml`: runs Ruff lint and format checks on open and updated pull requests
- `main-tests.yml`: runs smoke tests on pushes to `main` and uploads reports, logs, screenshots, and Allure results

## Notes

- Test environment values are stored in `config/config.ini`
- Failure screenshots and page source are attached through `pytest_runtest_makereport`
- Browser drivers are managed automatically through `webdriver-manager`
