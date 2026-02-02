"""Upshot Cards Automation - Login and button clicks"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
sys.path.append('c:\\PythonAutomation')
from web.web_source import (
    create_firefox_driver,
    find_element_by_selectors,
    click_element_safe,
    cleanup_all,
    run_all_batches,
    FIREFOX_PROFILES
)

# ==================== CONFIGURATION ====================
URL = "https://upshot.cards"
WAIT_AFTER_LOGIN = 12  # Tăng từ 10 lên 12
# ======================================================


def upshot_task(profile_path, profile_index):
    """Main task for Upshot Cards automation"""
    driver = None
    try:
        print(f"\n[Profile {profile_index}] Starting Upshot automation...")
        
        # Create driver and navigate
        driver = create_firefox_driver(profile_path,headless=False)
        driver.get(URL)
        time.sleep(7)  # Tăng từ 5 lên 7
        
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/button").click()
        time.sleep(2)  # Tăng từ 3 lên 5
        # Step 1: Click Google login button in modal
        print(f"[Profile {profile_index}] Step 1: Looking for Google login button...")
        google_selectors = [
            "//button[contains(., 'Continue with Google')]",
            "//button[contains(., 'Google')]",
            "//button[contains(., 'Sign in with Google')]",
            "//*[contains(@class, 'google')]//button",
            "//button[.//text()[contains(., 'Google')]]"
        ]
        
        google_button = find_element_by_selectors(driver, google_selectors, wait_time=10)
        if google_button:
            driver.execute_script("arguments[0].scrollIntoView(true);", google_button)
            time.sleep(3)  # Tăng từ 1 lên 3
            google_button.click()
            print(f"[Profile {profile_index}] Clicked Google login button")
            time.sleep(7)  # Tăng từ 5 lên 7
            
            # Select Google account
            account_selectors = [
                "//li[1]//div[@role='link']",
                "//div[@data-authuser='0']",
                "//ul//li[1]//div[contains(@class, 'BHzsHc')]",
                "(//div[contains(@jsname, 'V67aGc')])[1]"
            ]
            
            google_account = find_element_by_selectors(driver, account_selectors, wait_time=5)
            if google_account:
                google_account.click()
                print(f"[Profile {profile_index}] Selected Google account")
                time.sleep(5)  # Tăng từ 3 lên 5
            
            # Wait after login
            print(f"[Profile {profile_index}] Waiting {WAIT_AFTER_LOGIN}s after login...")
            time.sleep(WAIT_AFTER_LOGIN)
        else:
            print(f"[Profile {profile_index}] Google login button not found, may already be logged in")

        
        # Step 2: Close modal by clicking X button
        print(f"[Profile {profile_index}] Step 2: Closing modal...")
        close_selectors = [
            "//button[contains(@class, 'close') or contains(@aria-label, 'close') or contains(@aria-label, 'Close')]",
            "//button[text()='×' or text()='X']",
            "//*[@role='button'][text()='×' or text()='X']",
            "//button[contains(., '×')]"
        ]
        
        close_button = find_element_by_selectors(driver, close_selectors, wait_time=5)
        if close_button:
            click_element_safe(driver, close_button)
            print(f"[Profile {profile_index}] Modal closed")
            time.sleep(4)  # Tăng từ 2 lên 4
        else:
            print(f"[Profile {profile_index}] Close button not found, modal may have auto-closed")
        
        # Step 3: Click the three buttons in sequence
        print(f"[Profile {profile_index}] Step 3: Clicking buttons...")
        
        # Button 1
        try:
            button1 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[2]/div[1]/div[1]/button"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button1)
            time.sleep(3)  # Tăng từ 1 lên 3
            click_element_safe(driver, button1)
            print(f"[Profile {profile_index}] Clicked button 1")
            time.sleep(4)  # Tăng từ 2 lên 4
        except Exception as e:
            print(f"[Profile {profile_index}] Error clicking button 1: {str(e)}")
        
        # Button 2
        try:
            button2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[2]/div[1]/div[2]/button"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button2)
            time.sleep(3)  # Tăng từ 1 lên 3
            click_element_safe(driver, button2)
            print(f"[Profile {profile_index}] Clicked button 2")
            time.sleep(4)  # Tăng từ 2 lên 4
        except Exception as e:
            print(f"[Profile {profile_index}] Error clicking button 2: {str(e)}")
        
        # Button 3
        try:
            button3 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[1]/div[2]/div[2]/div/div[2]/div/button"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button3)
            time.sleep(3)  # Tăng từ 1 lên 3
            click_element_safe(driver, button3)
            print(f"[Profile {profile_index}] Clicked button 3")
            time.sleep(4)  # Tăng từ 2 lên 4
        except Exception as e:
            print(f"[Profile {profile_index}] Error clicking button 3: {str(e)}")
        
        print(f"[Profile {profile_index}] Task completed successfully!")
        time.sleep(5)  # Tăng từ 3 lên 5
        
        return True
        
    except Exception as e:
        print(f"[Profile {profile_index}] Error: {str(e)}")
        return False
        
    finally:
        if driver:
            driver.quit()
        cleanup_all(profile_path, profile_index)


def main():
    """Run automation for all profiles in batches"""
    print("="*60)
    print("UPSHOT CARDS AUTOMATION")
    print("="*60)
    print(f"URL: {URL}")
    print(f"Total profiles: {len(FIREFOX_PROFILES)}")
    print("="*60)
    
    # Run all batches (8+8+6 profiles)
    results = run_all_batches(upshot_task, FIREFOX_PROFILES, wait_between_batches=8)
    
    # Summary
    success = sum(1 for r in results if r)
    print("\n" + "="*60)
    print(f"COMPLETED: {success}/{len(results)} profiles successful")
    print("="*60)


if __name__ == "__main__":
    main()