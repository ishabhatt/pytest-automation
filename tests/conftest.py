import configparser
from datetime import datetime
from pathlib import Path

import allure
import pytest
from pytest_metadata.plugin import metadata_key

from drivers.driver_factory import DriverFactory

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT_DIR / "config" / "config.ini"
SCREENSHOT_DIR = ROOT_DIR / "screenshots"


@pytest.fixture()
def setup(browser, request):
    driver = None
    headless = request.config.getoption("--headless")

    driver = DriverFactory.create_driver(browser=browser, headless=headless)

    request.node.driver = driver
    yield driver

    driver.quit()


@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture()
def env_config(request):
    env = request.config.getoption("--env")
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if env not in config:
        raise ValueError(f"Environment '{env}' not found in config.ini")
    return config[env]


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="browser type: chrome (default), firefox, edge",
    )
    parser.addoption(
        "--env",
        default="dev",
        help="Environment to run tests against: dev (default), qa, stage, or prod",
    )
    parser.addoption(
        "--headless", action="store_true", help="Run browser in headless mode"
    )


############### pytest HTML Report #################
def pytest_html_report_title(report):
    report.title = "Pytest HTML Report"


def pytest_metadata(metadata):
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Plugins", None)


def pytest_configure(config):
    config.stash[metadata_key]["Project"] = "Pytest Automation"
    config.stash[metadata_key]["Tester Name"] = "Isha"
    report_path = (
        ROOT_DIR / "reports" / (datetime.now().strftime("%d%m%Y-%H%M%S") + ".html")
    )
    config.option.htmlpath = report_path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots and attach them to Allure and pytest-html."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    driver = getattr(item, "driver", None)
    if driver is None:
        return

    SCREENSHOT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%d%m%Y-%H%M%S")
    filename = f"{item.name}_{timestamp}.png"
    screenshot_path = SCREENSHOT_DIR / filename
    driver.save_screenshot(str(screenshot_path))

    ## Attach screenshot to allure report
    allure.attach.file(
        str(screenshot_path),
        name=f"{item.name}_failure",
        attachment_type=allure.attachment_type.PNG,
    )

    ## Attach page source to allure report
    allure.attach(
        driver.page_source,
        name="page_source",
        attachment_type=allure.attachment_type.HTML,
    )
