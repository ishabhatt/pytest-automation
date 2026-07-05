import logging

import allure
import pytest

from pages.login_page import LoginPage


class TestLoginError:
    logger = logging.getLogger()

    @allure.epic("Login")
    @allure.feature("Authentication")
    @allure.story("Locked User Login")
    @pytest.mark.smoke
    def test_login_locked_user(self, setup, env_config):
        self.logger.info("****TC0002 : Test Locked User Login****")
        self.driver = setup
        with allure.step("Open Application URL"):
            self.driver.get(env_config["baseURL"])
            self.logger.info("* Open Browser and go to url")
            self.driver.maximize_window()

        self.login_page = LoginPage(self.driver)
        with allure.step("Login as locked user"):
            self.logger.info("* Enter locked username and password")
            self.login_page.enter_username("locked_out_user")
            self.login_page.enter_password(env_config["password"])
        with allure.step("Click Login"):
            self.login_page.submit()

        with allure.step("Verify Login error"):
            self.logger.info("* Verify Error displayed")
            assert self.login_page.is_error_visible(), (
                "Expected login error not visible"
            )
            error_message = self.login_page.get_error()
            assert "Oops, this user has been locked out." in error_message, (
                f"Unexpected error message: {error_message}"
            )

        self.logger.info("**** FINISH TEST TC0002 : Test Locked User Login ****")
