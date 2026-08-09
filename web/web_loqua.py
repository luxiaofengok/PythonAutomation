from web_source import (
    create_firefox_driver,
    check_and_login,
    login_with_google,
    find_element_by_selectors,
    click_element_safe,
    FIREFOX_PROFILES,
    run_all_batches,
    scroll_to_element
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#==================== CONFIGURATION ====================
LOQUA_URL = "https://loqua.net/daily-check-in"
#========================================================

def access_loqua(driver, profile_index):
    """Step N1: Access https://loqua.net/daily-check-in"""
    try:
        print(f"[Profile {profile_index}] [N1] Accessing {LOQUA_URL}...")
        driver.get(LOQUA_URL)

        # Wait for page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)

        print(f"[Profile {profile_index}] [N1] Page loaded successfully")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] [N1] Error accessing page: {str(e)}")
        return False


def login_and_checkin_loqua(driver, profile_index):

    Connect_selectors = [
        "//*[@id='root']/main/div/section[12]/div[2]/button",
        "//button[contains(., 'Connect to Check In')]",
    ]
    Conect_button = find_element_by_selectors(driver, Connect_selectors, 15)
    if Conect_button:
        scroll_to_element(driver, Conect_button)
        click_element_safe(driver, Conect_button)
        time.sleep(2)

    
    main_window = driver.current_window_handle
 
    google_selectors = [
        "//button[contains(., 'Continue with Google')]",
        "//button[contains(., 'Google')]",
        "//button[contains(., 'Sign in with Google')]",
        "//*[contains(@class, 'google')]//button",
        "//button[.//text()[contains(., 'Google')]]",
    ]

    google_button = find_element_by_selectors(driver, google_selectors,5)
    if not google_button:
        print(f"[Profile {profile_index}] Google button not found")
        return False

    scroll_to_element(driver, google_button)
    google_button.click()
    time.sleep(3)

    all_windows = driver.window_handles
    for window in all_windows:
        if window != main_window:
            driver.switch_to.window(window)
            print(f"[Profile {profile_index}] Switched to Google login window")
            break

    time.sleep(3)

        # ------------------------------------------------------------------
        # 2️⃣  Select the Google account (first one by default)
        # ------------------------------------------------------------------
    account_selectors = [
        "//li[1]//div[@role='link']",
        "//div[@data-authuser='0']",
        "//ul//li[1]//div[contains(@class, 'BHzsHc')]",
        "(//div[contains(@jsname, 'V67aGc')])[1]",
    ]

    google_account = find_element_by_selectors(
        driver, account_selectors, 5
    )
    if google_account:
        scroll_to_element(driver, google_account)
        google_account.click()
        time.sleep(3)
    else:
        print(f"[Profile {profile_index}] Google account not found")
        return False

    continue_selectors = [
        "//button[contains(., 'Continue')]",
        "//button[contains(., 'Tiếp tục')]",
    ]

    continue_button = find_element_by_selectors(
        driver, continue_selectors, 5
    )
    if continue_button:
        scroll_to_element(driver, continue_button)
        continue_button.click()
        time.sleep(3)


    driver.switch_to.window(main_window)
    time.sleep(15)

    Check_in_selectors = [
        "//*[@id='root']/main/div/section[12]/div[2]/button",
        "//button[contains(., 'Check In')]",
    ]
    Check_in_button = find_element_by_selectors(driver, Check_in_selectors, 5)
    if Check_in_button:
        scroll_to_element(driver, Check_in_button)
        click_element_safe(driver, Check_in_button)
        time.sleep(5)
        print(f"[Profile {profile_index}] Check-in completed")

    return True

def run_loqua_script(profile_path, profile_index):
    """Chạy automation script cho Loqua"""
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"\n[Profile {profile_index}] Starting Loqua automation...")
        print(f"{'='*60}")
        driver = create_firefox_driver(profile_path)
        
        if not access_loqua(driver, profile_index):
            return False
        
        if not login_and_checkin_loqua(driver, profile_index):
            return False
        
        
        print(f"[Profile {profile_index}] Loqua automation completed successfully")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] Error: {str(e)}")
        return False

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


if __name__ == "__main__":

    results = run_all_batches(run_loqua_script, FIREFOX_PROFILES)
    total = len(results)
    success = sum(1 for r in results if r)
    print(f"\n{'='*60}")
    print(f"KẾT QUẢ TỔNG KẾT")
    print(f"{'='*60}")
    print(f"Tổng profiles: {total}")
    print(f"Thành công:    {success}")
    print(f"Thất bại:      {total - success}")
    print(f"{'='*60}")

    


    


