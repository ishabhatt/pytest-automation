from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class NavigationPage(BasePage):
    OPEN_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_MENU_ITEM = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        super().__init__(driver)

    def open_menu(self) -> None:
        self.wait_until_clickable(self.OPEN_MENU)
        self.click(self.OPEN_MENU)

    def is_menu_displayed(self) -> bool:
        return self.find_element(self.OPEN_MENU).is_displayed()

    def logout(self) -> None:
        self.open_menu()
        self.wait_until_clickable(self.LOGOUT_MENU_ITEM)
        self.click(self.LOGOUT_MENU_ITEM)
