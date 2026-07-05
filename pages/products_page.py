from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductsPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, "span.title")

    def __init__(self, driver):
        super().__init__(driver)

    def get_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)
