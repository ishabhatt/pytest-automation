from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def get_url(self) -> str:
        return self.driver.current_url

    def find_element(self, locator) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def get_text(self, locator) -> str:
        return self.find_element(locator).text

    def click(self, locator) -> None:
        self.find_element(locator).click()

    def wait_until_clickable(self, locator) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_until_visible(self, locator) -> WebElement:
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )
