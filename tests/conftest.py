import configparser
from datetime import datetime
from pathlib import Path

import allure
import pytest
from pytest_metadata.plugin import metadata_key
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT_DIR / "config" / "config.ini"
SCREENSHOT_DIR = ROOT_DIR / "screenshots"


@pytest.fixture()
def setup(browser, request):
    driver = None
    headless = request.config.getoption("--headless")
    if browser == "firefox":
        print("Launching Firefox")
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        serviceObj = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=serviceObj, options=options)
    elif browser == "edge":
        print("Launching Edge")
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        serviceObj = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=serviceObj, options=options)
    else:
        print("Launching Chrome")
        options = webdriver.ChromeOptions()
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        }
        options.add_experimental_option("prefs", prefs)
        if headless:
            options.add_argument("--headless=new")
        serviceObj = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=serviceObj, options=options)
    request.node.driver = driver
    yield driver
    if driver:
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
