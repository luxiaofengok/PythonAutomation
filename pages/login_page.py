from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from utils.config_reader import ConfigReader


class LoginPage():
    def __init__(self, driver):
        self.driver1 = driver
        self.username = (By.NAME,"username")
        self.password = (By.NAME,"password")
        self.lgn_btn = (By.XPATH,"//button[@type='submit']")
        
    def enter_username(self, username):
        self.driver1.find_element(*self.username).send_keys(username)
    def enter_password(self, password):
        self.driver1.find_element(*self.password).send_keys(password)
    def click_login_button(self):
        self.driver1.find_element(*self.lgn_btn).click()
    def get_error_message(self):
        return self.driver1.find_element(By.XPATH,"//oxd-text oxd-text--p oxd-alert-content-text").text==("Invalid credentials")
    
    def do_login(self, username ,password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
        