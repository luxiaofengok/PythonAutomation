"""Blend Money Automation - Daily Reward Claiming"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Import common utilities from web_source
from web_source import (
    create_firefox_driver,
    find_element_by_selectors,
    click_element_safe,
    login_with_google,
    cleanup_all,
    run_all_batches,
    FIREFOX_PROFILES
)

# ==================== TIMING CONFIGURATION ====================
WAIT_PAGE_LOAD = 15         # Chờ sau khi load trang
WAIT_AFTER_LOGIN = 5        # Chờ sau khi login
WAIT_RELOAD = 15            # Chờ sau khi reload
WAIT_MODAL = 3             # Chờ modal hiện
WAIT_BEFORE_CLOSE = 12       # Chờ trước khi đóng browser
ELEMENT_TIMEOUT = 10        # Timeout tìm element (giây)
# ============================================================

BLEND_URL = "https://app.blend.money/dashboard/usdc"

def blend_money_automation(profile_path, profile_index):
    """
    Main automation function for Blend Money
    Args:
        profile_path: Firefox profile path
        profile_index: Profile number for logging
    """
    driver = None
    try:
        print(f"\n[Profile {profile_index}] Starting Blend Money automation...")
        
        # Create driver
        driver = create_firefox_driver(profile_path, optimize=True, headless=False)
        
        # Step 1: Open page and wait for elements to load
        print(f"[Profile {profile_index}] Opening {BLEND_URL}...")
        driver.get(BLEND_URL)
        time.sleep(WAIT_PAGE_LOAD)
        
        # Find and click login button
        print(f"[Profile {profile_index}] Proceeding with login...")
        login_selectors = [
            "//button[contains(., 'Login')]",
            "//*[contains(@class, 'login')]//button",
            "//button[contains(., 'Log in')]"
        ]
        
        login_button = find_element_by_selectors(driver, login_selectors, ELEMENT_TIMEOUT)
        if login_button:
            print(f"[Profile {profile_index}] Clicking login button...")
            click_element_safe(driver, login_button)
            time.sleep(2)
        else:
            print(f"[Profile {profile_index}] Login button not found")
        
        # Login with Google
        print(f"[Profile {profile_index}] Attempting Google login...")
        if not login_with_google(driver, profile_index):
            print(f"[Profile {profile_index}] Google login failed")
            return False
        
        time.sleep(WAIT_AFTER_LOGIN)
        
        # Step 2: Reload page after login
        print(f"[Profile {profile_index}] Reloading page...")
        driver.refresh()
        time.sleep(WAIT_RELOAD)
        
        # Find and click Daily Reward button
        print(f"[Profile {profile_index}] Looking for Daily Reward button...")
        daily_reward_selectors = [
            "//button[contains(., 'Daily Reward')]",
            "//button[contains(., 'Daily')]",
            "//button[contains(., 'Reward')]",
            "//*[contains(text(), 'Daily Reward')]",
            "//*[contains(@class, 'daily')]//button",
        ]
        
        daily_button = find_element_by_selectors(driver, daily_reward_selectors, ELEMENT_TIMEOUT)
        if not daily_button:
            print(f"[Profile {profile_index}] Daily Reward button not found")
            return False
        
        print(f"[Profile {profile_index}] Clicking Daily Reward button...")
        click_element_safe(driver, daily_button)
        time.sleep(WAIT_MODAL)
        
        # Step 3: Click View Reward button in modal
        print(f"[Profile {profile_index}] Looking for View Reward button...")
        view_reward_selectors = [
            "//button[contains(., 'View Reward')]",
            "//button[contains(., 'View')]",
            "//*[contains(@class, 'modal')]//button[contains(., 'View')]",
        ]
        
        view_button = find_element_by_selectors(driver, view_reward_selectors, ELEMENT_TIMEOUT)
        if not view_button:
            print(f"[Profile {profile_index}] View Reward button not found")
            return False
        
        print(f"[Profile {profile_index}] Clicking View Reward button...")
        click_element_safe(driver, view_button)
        time.sleep(WAIT_BEFORE_CLOSE)
        
        print(f"[Profile {profile_index}] ✓ Completed successfully!")
        return True
        
    except Exception as e:
        print(f"[Profile {profile_index}] ✗ Error: {str(e)}")
        return False
        
    finally:
        if driver:
            print(f"[Profile {profile_index}] Closing browser...")
            driver.quit()
        cleanup_all(profile_path, profile_index)


def main():
    """Run automation for all profiles in batches"""
    print("\n" + "="*60)
    print("BLEND MONEY - DAILY REWARD AUTOMATION")
    print("="*60)
    
    # Run all batches (8+8+6 profiles)
    results = run_all_batches(
        task_function=blend_money_automation,
        profiles=FIREFOX_PROFILES,
        wait_between_batches=8
    )
    
    # Summary
    successful = sum(1 for r in results if r)
    failed = len(results) - successful
    
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    print(f"Total profiles: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()