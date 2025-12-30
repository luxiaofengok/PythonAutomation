from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pytest

def test_dropdown(driver):
    select= Select(driver.find_element(By.ID,"dropdown"))
    select.select_by_visible_text("Option 1")
    sleep(2)
    select.select_by_value("2")
    sleep(2)
    

    

