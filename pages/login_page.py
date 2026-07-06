from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.products_page import ProductsPage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MSG = (By.CSS_SELECTOR, ".error-message-container")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_username(self, username: str) -> None:
        self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        self.type_text(self.PASSWORD_INPUT, password)

    def submit(self) -> None:
        self.click(self.LOGIN_BUTTON)

    def is_error_visible(self) -> bool:
        return self.find_element(self.ERROR_MSG).is_displayed()

    def get_error(self) -> str:
        return self.get_text(self.ERROR_MSG)

    def login(self, username, password) -> ProductsPage:
        self.enter_username(username)
        self.enter_password(password)
        self.submit()
        assert "inventory.html" in self.get_url()
        return ProductsPage(self.driver)
