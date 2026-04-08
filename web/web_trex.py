"""T-Rex Quest Automation - Web automation for https://www.trex.xyz/portal/quest"""

from web_source import (
    create_firefox_driver,
    check_and_login,
    find_element_by_selectors,
    click_element_safe,
    FIREFOX_PROFILES,
    run_all_batches
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ==================== CONFIGURATION ====================
TREX_URL = "https://www.trex.xyz/portal/quest"
CHECKIN_BUTTON_XPATH = "/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/button"

# Indicators that show user is logged in
LOGGED_IN_INDICATORS = [
    "//button[contains(., 'Checkin')]",
    "//button[contains(., 'Check in')]",
    "//button[contains(., 'Log out')]",
    "//button[contains(., 'Logout')]",
    "//div[@class='user-profile']",
    "//span[contains(@class, 'username')]"
]
# ========================================================


def access_trex_quest(driver, profile_index=0):
    """Step B1: Access https://www.trex.xyz/portal/quest"""
    try:
        print(f"[Profile {profile_index}] [B1] Accessing {TREX_URL}...")
        driver.get(TREX_URL)

        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)

        print(f"[Profile {profile_index}] [B1] Page loaded successfully")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] [B1] Error accessing page: {str(e)}")
        return False


def click_login_and_google(driver, profile_index=0):
    """Step B2: Click login button, then login with Google (handle popup)"""
    try:
        print(f"[Profile {profile_index}] [B2] Starting login process...")

        # Store main window handle
        main_window = driver.current_window_handle

        # Find and click login button
        login_selectors = [
            "//button[contains(., 'Login')]",
            "//button[contains(., 'login')]",
            "//button[contains(., 'Sign in')]",
            "//button[contains(., 'Log in')]",
            "//a[contains(., 'Login')]"
        ]

        login_button = find_element_by_selectors(driver, login_selectors, 5)
        if not login_button:
            print(f"[Profile {profile_index}] [B2] Login button not found")
            return False

        print(f"[Profile {profile_index}] [B2] Found login button, clicking...")
        click_element_safe(driver, login_button)
        time.sleep(3)

        # Find and click Google login button
        google_selectors = [
            "/html/body/div[2]/div/div[2]/div/div/div[1]/div[1]/button",
            "//button[contains(., 'Continue with Google')]",
            "//button[contains(., 'Google')]",
            "//button[contains(., 'Sign in with Google')]"
        ]

        google_button = find_element_by_selectors(driver, google_selectors, 5)
        if not google_button:
            print(f"[Profile {profile_index}] [B2] Google button not found")
            return False

        print(f"[Profile {profile_index}] [B2] Found Google button, clicking...")
        driver.execute_script("arguments[0].scrollIntoView(true);", google_button)
        time.sleep(1)
        click_element_safe(driver, google_button)
        time.sleep(3)

        # Handle Google popup window
        print(f"[Profile {profile_index}] [B2] Waiting for Google popup...")
        time.sleep(3)

        # Get all window handles
        all_windows = driver.window_handles
        if len(all_windows) > 1:
            # Switch to Google popup
            for window in all_windows:
                if window != main_window:
                    print(f"[Profile {profile_index}] [B2] Switching to Google popup window...")
                    driver.switch_to.window(window)
                    time.sleep(3)
                    break

            # Try to select Google account
            account_selectors = [
                "//li[1]//div[@role='link']",
                "//div[@data-authuser='0']",
                "//ul//li[1]//div[contains(@class, 'BHzsHc')]",
                "(//div[contains(@jsname, 'V67aGc')])[1]",
                "//li[@data-authuser='0']"
            ]

            google_account = find_element_by_selectors(driver, account_selectors, 5)
            if google_account:
                print(f"[Profile {profile_index}] [B2] Clicking Google account...")
                google_account.click()
                time.sleep(3)

            # Click continue button if present
            continue_selectors = [
                "//button[contains(., 'Continue')]",
                "//button[contains(., 'Tiếp tục')]",
                "//button[contains(., 'Xác nhận')]"
            ]
            continue_button = find_element_by_selectors(driver, continue_selectors, 3)
            if continue_button:
                print(f"[Profile {profile_index}] [B2] Clicking continue button...")
                continue_button.click()
                time.sleep(3)

            # Switch back to main window
            print(f"[Profile {profile_index}] [B2] Switching back to main window...")
            driver.switch_to.window(main_window)
            time.sleep(5)

            # Wait for page to be ready
            print(f"[Profile {profile_index}] [B2] Waiting for page to load...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)
        else:
            print(f"[Profile {profile_index}] [B2] No popup detected, proceeding...")

        print(f"[Profile {profile_index}] [B2] Google login completed")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] [B2] Login error: {str(e)}")
        # Try to switch back to main window
        try:
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass
        return False


def click_checkin_button(driver, profile_index=0):
    """Step B3: Click the Checkin button"""
    try:
        print(f"[Profile {profile_index}] [B3] Looking for Checkin button...")

        # Wait longer for page to settle after login
        time.sleep(3)

        # Try multiple XPath selectors for checkin button
        checkin_selectors = [
            CHECKIN_BUTTON_XPATH,  # Original XPath
            "//button[contains(., 'Checkin')]",
            "//button[contains(., 'Check in')]",
            "//button[contains(., 'CHECK IN')]",
            "//button[contains(., 'Checkin')]",
            "//button[@class[contains(., 'checkin')]]",
            "(//button)[1]"
        ]

        checkin_button = None
        for selector in checkin_selectors:
            try:
                checkin_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"[Profile {profile_index}] [B3] Found button with selector: {selector}")
                break
            except:
                continue

        if not checkin_button:
            print(f"[Profile {profile_index}] [B3] Checkin button not found with any selector")
            print(f"[Profile {profile_index}] [B3] Listing all buttons on page:")
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            for i, btn in enumerate(all_buttons):
                print(f"  Button {i}: '{btn.text}' - Tag: {btn.tag_name}")
            return False

        print(f"[Profile {profile_index}] [B3] Found Checkin button, clicking...")
        driver.execute_script("arguments[0].scrollIntoView(true);", checkin_button)
        time.sleep(1)
        click_element_safe(driver, checkin_button)

        print(f"[Profile {profile_index}] [B3] Checkin button clicked successfully")
        time.sleep(3)
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] [B3] Error clicking checkin button: {str(e)}")
        return False


def execute_trex_quest (profile_path, profile_index):
    """
    Execute complete T-Rex Quest automation:
    B1: Access quest page
    B2: Login with Google
    B3: Click Checkin button
    """
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"[Profile {profile_index}] Starting T-Rex Quest automation")
        print(f"{'='*60}")

        # Create driver
        driver = create_firefox_driver(profile_path)

        # B1: Access T-Rex Quest page
        if not access_trex_quest(driver, profile_index):
            print(f"[Profile {profile_index}] Failed at step B1")
            return False

        time.sleep(1)

        # B2: Click login and perform Google login
        if not click_login_and_google(driver, profile_index):
            print(f"[Profile {profile_index}] Failed at step B2")
            return False

        time.sleep(1)

        # B3: Click Checkin button
        if not click_checkin_button(driver, profile_index):
            print(f"[Profile {profile_index}] Failed at step B3")
            return False

        print(f"[Profile {profile_index}] All steps completed successfully!")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] Unexpected error: {str(e)}")
        return False
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


# Quick usage
if __name__ == "__main__":
    print("T-Rex Quest Automation")
    print("=" * 60)
    print("Usage:")
    print("1. Single profile: execute_trex_quest(profile_path, profile_index)")
    print("2. Batch mode: run_all_batches(execute_trex_quest)")
    print("=" * 60)

    # Example: Run with first profile only
    # result = execute_trex_quest(FIREFOX_PROFILES[0], 1)

    # Example: Run all batches
    results = run_all_batches(execute_trex_quest)
