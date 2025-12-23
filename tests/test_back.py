import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest


def test_navigator(driver):
    time.sleep(5)# import time
    print(driver.title)
    time.sleep(5)  # import time
    driver.get("https://google.com")
    time.sleep(5)  # import time
    print(driver.title)
    driver.current_url
    time.sleep(5)
    driver.back()
    driver.current_window_handle
    time.sleep(5)


        
        
        