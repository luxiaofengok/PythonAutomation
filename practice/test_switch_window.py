from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from time import sleep

class TestSwitchNewWindow:
    def test_open_and_switch_new_window(self):
        url = "https://www.letskodeit.com/practice"
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        # locate the Open Window button by text (fallback to id if needed)
        try:
            open_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(normalize-space(), 'Open Window')]")
                )
            )
        except Exception:
            open_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "openwindow"))
            )

        # store original handle and click to open a new window
        original_handle = driver.current_window_handle
        open_btn.click()

        # wait for a new window handle to appear
        wait.until(lambda d: len(d.window_handles) > 1)

        # find the new handle and switch to it
        new_handles = [h for h in driver.window_handles if h != original_handle]
        new_handle = new_handles[0]
        driver.switch_to.window(new_handle)

        # maximize the new window and sleep for observation
        driver.maximize_window()
        sleep(5)

        # optional: assert that we're not on the original window
        assert driver.current_window_handle == new_handle
