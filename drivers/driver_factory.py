# drivers/driver_factory.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class DriverFactory:
    @staticmethod
    def create_driver(browser: str, headless: bool = False) -> WebDriver:
        browser = browser.lower()

        if browser == "firefox":
            return DriverFactory._create_firefox_driver(headless)

        if browser == "edge":
            return DriverFactory._create_edge_driver(headless)

        return DriverFactory._create_chrome_driver(headless)

    @staticmethod
    def _create_chrome_driver(headless: bool) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        }
        options.add_experimental_option("prefs", prefs)

        if headless:
            options.add_argument("--headless=new")

        options.set_capability(
            "goog:loggingPrefs", {"browser": "ALL", "performance": "ALL"}
        )
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    @staticmethod
    def _create_firefox_driver(headless: bool) -> webdriver.Firefox:
        options = webdriver.FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    @staticmethod
    def _create_edge_driver(headless: bool) -> webdriver.Edge:
        options = webdriver.EdgeOptions()

        if headless:
            options.add_argument("--headless=new")

        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
