# pages/base_page.py
from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.retry import retry_on_exception

Locator = Tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.timeout = 10

    def get_url(self) -> str:
        return self.driver.current_url

    def find_element(self, locator: Locator) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def get_text(self, locator: Locator) -> str:
        return self.find_element(locator).text

    @retry_on_exception(attempts=3, delay=0.3)
    def click(self, locator: Locator) -> None:
        self.wait_until_clickable(locator).click()

    @retry_on_exception(attempts=2, delay=0.2)
    def type_text(self, locator: Locator, text: str) -> None:
        element = self.wait_until_visible(locator)
        element.clear()
        element.send_keys(text)

    def wait_until_clickable(self, locator: Locator) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_until_visible(self, locator: Locator) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )
