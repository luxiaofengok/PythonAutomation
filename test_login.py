import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

def test_login():
    driver=webdriver.Chrome()
    base_url="https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    driver.get(base_url)
    driver.maximize_window()
    #wait for SUT
    time.sleep(5)  # import time)  # import time
    driver.find_element(By.NAME,"username").send_keys("Admin")
    driver.find_element(By.NAME,"password").send_keys("admin123")
    #driver.find_element(By.CSS_SELECTOR,".oxd-button").click() # day la button login
    driver.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(5)# import time 
    assert driver.find_element(By.XPATH,"//h6").text == "Dashboard"