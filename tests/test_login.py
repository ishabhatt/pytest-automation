import logging

import allure
import pytest

from pages.login_page import LoginPage


class TestLogin:
    logger = logging.getLogger()

    @allure.epic("Login")
    @allure.feature("Authentication")
    @allure.story("Standard User Login")
    @pytest.mark.smoke
    def test_login(self, setup, env_config):
        self.logger.info("****TC0001 : Test Standard User Login****")
        driver = setup
        with allure.step("Open application"):
            driver.get(env_config["baseURL"])
            self.logger.info("* Open Browser and go to url")
        driver.maximize_window()

        login_page = LoginPage(driver)
        with allure.step("Login with valid credentials"):
            self.logger.info("* Enter valid username and password")
            product_page = login_page.login(
                env_config["username"], env_config["password"]
            )

        with allure.step("Verify Login is successful"):
            title = product_page.get_title()
            self.logger.info("* Verify Products are displayed")
            assert title == "Products", (
                f"Login Failed. Expected page title 'Products', but got '{title}'"
            )

        self.logger.info("**** FINISH TEST TC0001 : Test Standard User Login ****")
