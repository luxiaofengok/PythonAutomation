"""OnVoyage.ai Automation - Auto login and daily check-in"""

from web_source import *

# ==================== TIMING CONFIGURATION ====================
WAIT_PAGE_LOAD = 5          # Chờ sau khi load trang
WAIT_AFTER_LOGIN = 3        # Chờ sau khi click login
WAIT_GOOGLE_LOGIN = 4       # Chờ sau khi click Google login
WAIT_ACCOUNT_SELECT = 2     # Chờ sau khi chọn tài khoản
WAIT_BEFORE_CHECKIN = 3     # Chờ trước khi click check-in
WAIT_AFTER_CHECKIN = 3      # Chờ sau khi click check-in
WAIT_BEFORE_CLOSE = 8       # Chờ trước khi đóng browser
WAIT_BETWEEN_BATCHES = 8    # Chờ giữa các batch
ELEMENT_TIMEOUT = 30        # Timeout tìm element (giây)
# ============================================================

ONVOYAGE_URL = "https://app.onvoyage.ai/dashboard"


def onvoyage_automation(profile_path, profile_index):
    """
    OnVoyage automation for one profile:
    1. Access website
    2. Login with Google directly (no login check)
    3. Click DAILY CHECK-IN button
    """
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"[Profile {profile_index}] Starting OnVoyage automation")
        print(f"[Profile {profile_index}] Profile path: {profile_path}")
        print(f"{'='*60}\n")

        # Create driver
        print(f"[Profile {profile_index}] Creating Firefox driver...")
        driver = create_firefox_driver(profile_path, optimize=True)
        print(f"[Profile {profile_index}] Firefox driver created successfully")

        # Step 1: Access website
        print(f"[Profile {profile_index}] Accessing {ONVOYAGE_URL}")
        driver.get(ONVOYAGE_URL)
        time.sleep(WAIT_PAGE_LOAD)

        # Step 2: Login with Google directly (no login check)
        print(f"[Profile {profile_index}] Starting Google login...")

        # Save main window handle
        main_window = driver.current_window_handle
        print(f"[Profile {profile_index}] Main window saved")

        # Find and click Google login button
        print(f"[Profile {profile_index}] Looking for Google login button...")
        google_selectors = [
            "//button[contains(., 'Continue with Google')]",
            "//button[contains(., 'Google')]",
            "//button[contains(., 'Sign in with Google')]",
            "//*[contains(@class, 'google')]//button",
            "//button[.//text()[contains(., 'Google')]]",
            "//a[contains(., 'Google')]",
        ]

        google_button = find_element_by_selectors(driver, google_selectors, ELEMENT_TIMEOUT)
        if not google_button:
            print(f"[Profile {profile_index}] Google button not found")
            return False

        print(f"[Profile {profile_index}] Found Google button, clicking...")
        click_element_safe(driver, google_button)
        time.sleep(3)

        # Switch to new window (Google login popup)
        print(f"[Profile {profile_index}] Switching to Google login window...")
        all_windows = driver.window_handles
        for window in all_windows:
            if window != main_window:
                driver.switch_to.window(window)
                print(f"[Profile {profile_index}] Switched to Google login window")
                break

        # Select Google account in popup window
        print(f"[Profile {profile_index}] Looking for Google account selection...")
        time.sleep(3)

        account_selectors = [
            "//li[1]//div[@role='link']",
            "//div[@data-authuser='0']",
            "//ul//li[1]//div[contains(@class, 'BHzsHc')]",
            "(//div[contains(@jsname, 'V67aGc')])[1]",
            "//div[@role='link']",
        ]

        google_account = find_element_by_selectors(driver, account_selectors, 10)
        if google_account:
            print(f"[Profile {profile_index}] Found Google account, selecting...")
            click_element_safe(driver, google_account)
            time.sleep(WAIT_ACCOUNT_SELECT)
        else:
            print(f"[Profile {profile_index}] No account selection needed")

        # Click continue if present
        continue_selectors = [
            "//button[contains(., 'Continue')]",
            "//button[contains(., 'Tiếp tục')]",
        ]
        continue_button = find_element_by_selectors(driver, continue_selectors, 5)
        if continue_button:
            print(f"[Profile {profile_index}] Found continue button, clicking...")
            click_element_safe(driver, continue_button)
            time.sleep(2)

        # Wait for popup to close and switch back to main window
        print(f"[Profile {profile_index}] Waiting for login to complete...")
        time.sleep(WAIT_GOOGLE_LOGIN)

        # Switch back to main window
        print(f"[Profile {profile_index}] Switching back to main window...")
        driver.switch_to.window(main_window)
        print(f"[Profile {profile_index}] Login completed, back to main window")

        # Wait for page to reload after login
        print(f"[Profile {profile_index}] Waiting for page to reload after login...")
        time.sleep(5)

        # Step 3: Click DAILY CHECK-IN button
        print(f"[Profile {profile_index}] Looking for DAILY CHECK-IN button...")
        time.sleep(WAIT_BEFORE_CHECKIN)

        checkin_selectors = [
            "/html/body/div[1]/div/div[2]/div/aside/div[1]/div/div[2]/button",
            "//button[contains(., 'DAILY CHECK-IN')]",
            "//button[contains(., 'Daily Check')]",
            "//button[contains(., 'CHECK-IN')]",
            "//button[contains(., 'Check-in')]",
            "//aside//button",
        ]

        checkin_button = find_element_by_selectors(driver, checkin_selectors, ELEMENT_TIMEOUT)
        if checkin_button:
            print(f"[Profile {profile_index}] Found DAILY CHECK-IN button, clicking...")
            driver.execute_script("arguments[0].scrollIntoView(true);", checkin_button)
            time.sleep(1)
            click_element_safe(driver, checkin_button)
            time.sleep(WAIT_AFTER_CHECKIN)
            print(f"[Profile {profile_index}] DAILY CHECK-IN clicked successfully")
        else:
            print(f"[Profile {profile_index}] DAILY CHECK-IN button not found")
            return False

        # Final wait before closing
        print(f"\n[Profile {profile_index}] Automation completed! Waiting before closing...")
        time.sleep(WAIT_BEFORE_CLOSE)

        print(f"[Profile {profile_index}] Automation completed successfully")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] Error: {str(e)}")
        return False

    finally:
        if driver:
            print(f"[Profile {profile_index}] Closing browser...")
            try:
                driver.quit()
            except:
                pass
        cleanup_all(profile_path, profile_index)


def run_single_profile(profile_index=1):
    """Run automation for a single profile"""
    if profile_index < 1 or profile_index > len(FIREFOX_PROFILES):
        print(f"Invalid profile index. Use 1-{len(FIREFOX_PROFILES)}")
        return

    profile_path = FIREFOX_PROFILES[profile_index - 1]
    onvoyage_automation(profile_path, profile_index)


def run_all_profiles():
    """Run automation for all profiles in batches"""
    print("\n" + "="*60)
    print("ONVOYAGE.AI AUTOMATION - ALL PROFILES")
    print("="*60 + "\n")

    run_all_batches(
        task_function=onvoyage_automation,
        profiles=FIREFOX_PROFILES,
        wait_between_batches=WAIT_BETWEEN_BATCHES
    )

    print("\n" + "="*60)
    print("ALL PROFILES COMPLETED!")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_profiles()
