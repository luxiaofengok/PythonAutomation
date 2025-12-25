from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

def test_practice(driver):
    sleep(2)  # import time
    hiden_button= driver.find_element(By.ID, "hide-textbox")
    hiden_button.click()
    window_button =driver.find_element(By.CLASS_NAME,"img-fluid")
    driver.save_screenshot("screen.png")
    # hiden_button.screenshot("hidden.png")
    sleep(2)  # import time
    
    #using javascripts
    display_textbox = driver.find_element(By.ID,"displayed-text")
    driver.execute_script("arguments[0].value = 'Hello World!'", display_textbox)
    sleep(2)  # import time
    show_button= driver.find_element(By.ID, "show-textbox")
    show_button.click()
    sleep(2)  # import time
    