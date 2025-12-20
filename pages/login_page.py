from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class LoginPage():
    def __init__(self, driver):
        self.driver1 = driver
    def enter_username(self, username):
        self.driver1.find_element(By.NAME, "username").send_keys(username)
    def enter_username(self, password):
        self.driver1.find_element(By.NAME, "username").send_keys(password)
    def click_login_button(self):
        self.driver1.find_element(By.XPATH, "//button").click()
    def get_error_message(self):
        return self.driver1.find_element(By.XPATH,"//").text==("hihi")
        
        