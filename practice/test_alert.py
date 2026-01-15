from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from time import sleep


URL = "https://www.letskodeit.com/practice"
ALERT_BUTTON_ID = "alertbtn"  # Try ID selector instead

def test_alert():
    """Test: Navigate to page, click Alert button and accept the alert."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        driver.get(URL)
        sleep(2)  # Wait for page to load completely

        # Try finding button by ID first
        wait = WebDriverWait(driver, 10)
        btn = wait.until(EC.element_to_be_clickable((By.ID, ALERT_BUTTON_ID)))
        
        print(f"✓ Found button: {btn.text}")
        btn.click()

        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"✓ Alert text: {alert.text}")
        sleep(5)  # Wait to see the alert
        alert.accept()
        
        print("✅ Alert handled successfully")

    except Exception as e:
        print(f"❌ Error: {e}")
        # Try to find what buttons are available
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"\n⚠️ Found {len(buttons)} buttons on page:")
            for btn in buttons[:10]:  # Show first 10
                print(f"  - Text: '{btn.text}' | ID: '{btn.get_attribute('id')}' | Name: '{btn.get_attribute('name')}'")
        except:
            pass
        raise

    finally:
        sleep(2)  # Keep browser open for a while to see result
        driver.quit()


if __name__ == '__main__':
    test_alert()


