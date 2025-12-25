import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from pages.login_page import LoginPage

class TestLogin:
    def test_login_pass(driver):
        driver.username("admin")
        

