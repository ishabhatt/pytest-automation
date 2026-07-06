import logging
from typing import Dict

import allure
import pytest

from pages.login_page import LoginPage
from pages.navigation_page import NavigationPage
from utils.data_reader import DataReader

DATAFILE = "login_data.csv"


def login_data_ids(data):
    return f"{data['username']}-{data['result']}"


class TestLoginDatadriven:
    logger = logging.getLogger()

    @allure.epic("Login")
    @allure.feature("Authentication")
    @allure.story("Various User Login")
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "data",
        DataReader.load_csv_data(filename=DATAFILE),
        ids=login_data_ids,
    )
    def test_login_data(self, setup, env_config, data: Dict[str, str]) -> None:
        self.logger.info("****TC0003 : Test Users Login****")
        driver = setup
        with allure.step("Open Application URL"):
            driver.get(env_config["baseURL"])
            self.logger.info("* Open Browser and go to url")
            driver.maximize_window()

        login_page = LoginPage(driver)
        navigation_page = NavigationPage(driver)

        print(data)
        username = data["username"]
        password = data["password"]
        with allure.step("Enter Credentials : user: " + username):
            self.logger.info("* Enter username (" + username + ") and password")
            login_page.enter_username(username)
            login_page.enter_password(password)
        with allure.step("Click Login"):
            login_page.submit()

        if str(data["result"]).lower() == "valid":
            with allure.step("Verify login successful"):
                login_success = navigation_page.is_menu_displayed()
                self.logger.info("* login_success:: " + str(login_success))
                self.logger.info("* Verify Products are displayed")
                if login_success:
                    navigation_page.logout()
                else:
                    self.logger.info("* Login Failed")
                assert login_success, f"Login failed for user: {username}"
        elif str(data["result"]).lower() == "invalid":
            with allure.step("Verify login not allowed"):
                self.logger.info("* Verify Login Not Successful")
                is_error = login_page.is_error_visible()
                if not is_error:
                    login_success = navigation_page.is_menu_displayed()
                    if login_success:
                        navigation_page.logout()
                assert is_error, f"Invalid login was allowed for user: {username}"

        self.logger.info("**** FINISH TEST TC0003 : Test Users Login ****")
