from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest


def test_navigator(driver):
    sleep(5)
    print(driver.title)
    sleep(5)
    driver.get("https://google.com")
    sleep(5)
    print(driver.title)
    driver.current_url
    sleep(5)
    driver.back()
    driver.current_window_handle
    sleep(5)
    
        
        