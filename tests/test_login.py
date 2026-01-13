from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from pages.login_page import LoginPage
from utils.config_reader import ConfigReader

class TestLogin:
    def test_login(self, driver):
        login_page = LoginPage(driver)
        sleep(2)
        username= ConfigReader.get_username()
        password= ConfigReader.get_password()
        login_page.do_login(username, password)
         # Just for demonstration; use explicit waits in real tests
        sleep(5)
        waits_for_dashboard = driver.find_element(By.XPATH, "//h6[text()='Dashboard']")
        assert waits_for_dashboard.is_displayed(), "Login failed - Dashboard not displayed"
        