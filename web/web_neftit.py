"""Neftit Daily Claim Automation - https://www.neftit.xyz"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.web_source import (
    create_firefox_driver, 
    find_element_by_selectors,
    click_element_safe,
    check_and_login,
    cleanup_all,
    run_all_batches,
    FIREFOX_PROFILES
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ==================== TIMING CONFIGURATION ====================
WAIT_PAGE_LOAD = 5          # Chờ sau khi load trang
WAIT_AFTER_LOGIN = 5        # Chờ sau khi click login
WAIT_GOOGLE_LOGIN = 4       # Chờ sau khi click Google login
WAIT_ACCOUNT_SELECT = 2     # Chờ sau khi chọn tài khoản
WAIT_BEFORE_CLAIM = 3       # Chờ trước khi click claim
WAIT_AFTER_CLAIM = 3        # Chờ sau khi click claim
WAIT_BEFORE_CLOSE = 8       # Chờ trước khi đóng browser
WAIT_BETWEEN_BATCHES = 8    # Chờ giữa các batch
ELEMENT_TIMEOUT = 30        # Timeout tìm element (giây)
HEADLESS_MODE = False       # Chạy ở chế độ headless (ẩn trình duyệt)
# ============================================================

# Website URL
NEFTIT_URL = "https://www.neftit.xyz"

# Logged in indicators - để kiểm tra đã login hay chưa
LOGGED_IN_INDICATORS = [
    "//button[contains(., 'Daily Claim')]",
    "//button[contains(., 'Claim')]",
    "//*[contains(@class, 'profile')]",
    "//*[contains(@class, 'user')]",
]


def neftit_automation(profile_path, profile_index):
    """
    Automation task for Neftit daily claim
    Args:
        profile_path: Firefox profile path
        profile_index: Profile number for logging
    """
    driver = None
    try:
        print(f"[Profile {profile_index}] Starting Neftit automation...")
        
        # Step 0: Cleanup before starting
        cleanup_all(profile_path, profile_index)
        
        # Create driver
        driver = create_firefox_driver(profile_path, headless=HEADLESS_MODE)
        
        # Step 1: Access website
        print(f"[Profile {profile_index}] Accessing {NEFTIT_URL}")
        driver.get(NEFTIT_URL)
        time.sleep(WAIT_PAGE_LOAD)

        # Step 2: Check if need to login - Look for 'Login' button
        print(f"[Profile {profile_index}] Checking login status...")
        print(f"[Profile {profile_index}] Looking for 'Login' button...")
        login_selectors = [
            "//button[text()='Login']",
            "//button[contains(text(), 'Login')]",
            "//button[contains(., 'Login')]",
            "//*[@role='dialog']//button[contains(., 'Login')]",
            "//div[contains(@class, 'modal')]//button[contains(., 'Login')]",
        ]
        
        login_button = find_element_by_selectors(driver, login_selectors, ELEMENT_TIMEOUT)
        
        # If we found "Login" button, means we need to login
        if login_button:
            print(f"[Profile {profile_index}] Not logged in yet, starting login process...")
            print(f"[Profile {profile_index}] Clicking 'Login' button...")
            click_element_safe(driver, login_button)
            time.sleep(WAIT_AFTER_LOGIN + 5)  # Thêm thời gian chờ để popup hiện ra đầy đủ
            
            # Step 3: Click Google icon (hiện ra sau khi click Login)
            print(f"[Profile {profile_index}] Looking for Google icon...")
            google_selectors = [
                "//img[@alt='Google']",
                "//img[contains(@alt, 'google')]",
                "//button[contains(@aria-label, 'Google')]",
                "//button[contains(@aria-label, 'google')]",
                "//*[name()='svg' and contains(@class, 'google')]",
                "//div[contains(@class, 'google')]//parent::button",
                "//button[contains(., 'Google')]",
                "//button[.//img[@alt='Google']]",
                "//button[.//img[contains(@src, 'google')]]",
                "//*[contains(@class, 'social')]//button[1]",
                "(//*[contains(@role, 'button')]//img[@alt='Google'])[1]",
                "//div[contains(@class, 'login')]//button[1]",
                "//div[contains(@class, 'auth')]//button[1]",
            ]
            
            google_button = find_element_by_selectors(driver, google_selectors, ELEMENT_TIMEOUT)
            if not google_button:
                print(f"[Profile {profile_index}] ERROR: Google login button not found!")
                return False
            
            print(f"[Profile {profile_index}] Found Google button, clicking...")
            click_element_safe(driver, google_button)
            time.sleep(WAIT_GOOGLE_LOGIN)
            
            # Select Google account (first account)
            account_selectors = [
                "//li[1]//div[@role='link']",
                "//div[@data-authuser='0']",
                "//ul//li[1]//div[contains(@class, 'BHzsHc')]",
                "(//div[contains(@jsname, 'V67aGc')])[1]",
            ]
            
            google_account = find_element_by_selectors(driver, account_selectors, 10)
            if google_account:
                print(f"[Profile {profile_index}] Selecting Google account...")
                click_element_safe(driver, google_account)
                time.sleep(WAIT_ACCOUNT_SELECT)
            
            # Click continue if present
            continue_selectors = [
                "//button[contains(., 'Continue')]",
                "//button[contains(., 'Tiếp tục')]",
            ]
            continue_button = find_element_by_selectors(driver, continue_selectors, 5)
            if continue_button:
                print(f"[Profile {profile_index}] Clicking continue button...")
                click_element_safe(driver, continue_button)
                time.sleep(2)
            
            print(f"[Profile {profile_index}] Login completed successfully!")
        else:
            # Already logged in (no "Login" button found)
            print(f"[Profile {profile_index}] Already logged in, skipping login process...")
        
        # Step 4: Wait for page to load after login
        print(f"[Profile {profile_index}] Waiting for page to load...")
        time.sleep(WAIT_PAGE_LOAD)
        
        # Step 5: Click "Daily Claim" button
        print(f"[Profile {profile_index}] Looking for 'Daily Claim' button...")
        daily_claim_selectors = [
            "//button[contains(., 'Daily Claim')]",
            "//button[contains(text(), 'Daily Claim')]",
            "//*[contains(@class, 'daily')]//button",
            "//button[contains(., 'Claim')]",
        ]
        
        daily_claim_button = find_element_by_selectors(driver, daily_claim_selectors, ELEMENT_TIMEOUT)
        if daily_claim_button:
            print(f"[Profile {profile_index}] Clicking 'Daily Claim' button...")
            driver.execute_script("arguments[0].scrollIntoView(true);", daily_claim_button)
            time.sleep(1)
            click_element_safe(driver, daily_claim_button)
            time.sleep(WAIT_BEFORE_CLAIM)
        else:
            print(f"[Profile {profile_index}] 'Daily Claim' button not found")
        
        # Step 6: Click "Claim Today's Reward" button
        print(f"[Profile {profile_index}] Looking for 'Claim Today's Reward' button...")
        claim_reward_selectors = [
            "//button[contains(., \"Claim Today's Reward\")]",
            "//button[contains(., 'Claim Today')]",
            "//button[contains(., 'Claim Reward')]",
            "//button[contains(text(), 'Claim')]",
            "//*[@role='dialog']//button[contains(., 'Claim')]",
            "//div[contains(@class, 'modal')]//button[contains(., 'Claim')]",
        ]
        
        claim_reward_button = find_element_by_selectors(driver, claim_reward_selectors, ELEMENT_TIMEOUT)
        if claim_reward_button:
            print(f"[Profile {profile_index}] Clicking 'Claim Today's Reward' button...")
            click_element_safe(driver, claim_reward_button)
            time.sleep(WAIT_AFTER_CLAIM)
            print(f"[Profile {profile_index}] ✓ Daily claim completed successfully!")
        else:
            print(f"[Profile {profile_index}] 'Claim Today's Reward' button not found - may already be claimed")
        
        # Wait before closing
        time.sleep(WAIT_BEFORE_CLOSE)
        
        print(f"[Profile {profile_index}] Task completed!")
        return True
        
    except Exception as e:
        print(f"[Profile {profile_index}] Error: {str(e)}")
        return False
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        # Cleanup after task
        cleanup_all(profile_path, profile_index)


def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("NEFTIT DAILY CLAIM AUTOMATION")
    print("="*60 + "\n")
    
    # Run all batches with the automation task
    results = run_all_batches(
        task_function=neftit_automation,
        profiles=FIREFOX_PROFILES,
        wait_between_batches=WAIT_BETWEEN_BATCHES
    )
    
    # Summary
    successful = sum(1 for r in results if r)
    total = len(results)
    print("\n" + "="*60)
    print(f"SUMMARY: {successful}/{total} profiles completed successfully")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()