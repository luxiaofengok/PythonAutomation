from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
from tests.conftest import driver


class BasePage:
    def __init__(self,driver):
        self.driver =driver
    
    def find_element(self, locator):
        return self.driver.find_element(*locator)
    
    def click(self, locator):
        element = self.find_element(locator)
        try:
            element.click()
        except NoSuchElementException:
            element=self.wait_for_element_clickable(locator)
            element.click()
        
    def wait_for_element_clickable(self, locator ,timeout=None):
        wait=WebDriverWait(self,driver,timeout)
        return wait.until(EC.element_to_be_clickable(*locator))
    
    

    
    
