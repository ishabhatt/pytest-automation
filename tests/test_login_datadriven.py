import logging

import allure
import pytest

from pages.login_page import LoginPage
from pages.navigation_page import NavigationPage
from utils.data_reader import DataReader


class TestLoginDatadriven:
    logger = logging.getLogger()
    datafile = "login_data.csv"

    @allure.epic("Login")
    @allure.feature("Authentication")
    @allure.story("Various User Login")
    @pytest.mark.regression
    def test_login_data(self, setup, env_config):
        self.logger.info("****TC0003 : Test Users Login****")
        self.data = DataReader.load_csv_data(filename=self.datafile)
        status_list = []

        self.driver = setup
        with allure.step("Open Application URL"):
            self.driver.get(env_config["baseURL"])
            self.logger.info("* Open Browser and go to url")
            self.driver.maximize_window()

        self.login_page = LoginPage(self.driver)
        self.navigation_page = NavigationPage(self.driver)

        for data in self.data:
            print(data)
            username = data["username"]
            password = data["password"]
            with allure.step("Enter Credentials : user: " + username):
                self.logger.info("* Enter username (" + username + ") and password")
                self.login_page.enter_username(username)
                self.login_page.enter_password(password)
            with allure.step("Click Login"):
                self.login_page.submit()

            if str(data["result"]).lower() == "valid":
                with allure.step("Verify login successful"):
                    self.login_success = self.navigation_page.is_menu_displayed()
                    self.logger.info(
                        "* self.login_success:: " + str(self.login_success)
                    )
                    self.logger.info("* Verify Products are displayed")
                    if self.login_success:
                        status_list.append("Pass")
                        self.navigation_page.logout()
                    else:
                        status_list.append("Fail")
                        self.logger.info("* Login Failed")
            elif str(data["result"]).lower() == "invalid":
                with allure.step("Verify login not allowed"):
                    self.logger.info("* Verify Login Not Successful")
                    self.is_error = self.login_page.is_error_visible()
                    if self.is_error:
                        status_list.append("Pass")
                    else:
                        status_list.append("Fail")
                        self.login_success = self.navigation_page.is_menu_displayed()
                        if self.login_success:
                            self.navigation_page.logout()
        # final test case validation
        assert "Fail" not in status_list, f"Some login scenarios failed: {status_list}"

        self.logger.info("**** FINISH TEST TC0003 : Test Users Login ****")
