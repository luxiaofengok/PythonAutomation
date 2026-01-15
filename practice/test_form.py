from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from time import sleep


class TestSubmitForm:
    def test_login_form(self):

        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("http://the-internet.herokuapp.com/login")
        wait = WebDriverWait(driver, 10)

        # wait and fill username
        username_el = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username_el.send_keys("tomsmith")

        # wait and fill password
        password_el = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_el.send_keys("SuperSecretPassword!")

        # submit the form using submit() on an element inside the form
        # (Selenium will submit the nearest enclosing form)
        username_el.submit()

        # verify we arrived at secure area
        wait.until(EC.url_contains("/secure"))
        assert "Secure Area" in driver.page_source
        
        