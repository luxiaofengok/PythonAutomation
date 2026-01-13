from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from time import sleep


URL = "https://www.letskodeit.com/practice"
ALERT_BUTTON_XPATH = "//button[contains(normalize-space(), 'Alert') or contains(@id,'alert')]"
def run_alert(url=URL, wait_alert_btn=10, wait_for_alert=2):
    driver = webdriver.Chrome()
    driver.maximize_window()
    """Navigate to page, click Alert button and accept the alert."""
    try:
        driver.get(url)

        wait = WebDriverWait(driver, wait_alert_btn)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, ALERT_BUTTON_XPATH)))
        btn.click()

        WebDriverWait(driver, wait_for_alert).until(EC.alert_is_present())
        driver.switch_to.alert.accept()

    finally:
        driver.quit()


if __name__ == '__main__':
    run_alert()


