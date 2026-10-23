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
LOGIN_URL = "https://thor.savethelife.io/auth/login"
#========================================================

def access_savethelife(driver, profile_index):
    """Step N1: Access https://thor.savethelife.io/auth/login"""
    try:
        print(f"[Profile {profile_index}] [N1] Accessing {LOGIN_URL}...")
        driver.get(LOGIN_URL)

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

def login_and_checkin_savethelife(driver, profile_index):
    time.sleep(5)

    login_with_google(driver, profile_index)
    time.sleep(10)  # Wait for login to complete

    Check_in_selectors = [
        "/html/body/div[2]/div/main/div/div[3]/button",
        "//button[contains(., 'Check in today (+500 Credits)')]"
    ]

    check_in_button = find_element_by_selectors(driver, Check_in_selectors, 5)

    if check_in_button:
        scroll_to_element(driver, check_in_button)
        click_element_safe(driver, check_in_button)
        print(f"[Profile {profile_index}] [N2] Check-in button clicked successfully")
    

    time.sleep(5)  # Wait for any post-check-in actions to complete
    return True


def run_savethelife_script(profile_path, profile_index):
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"[Profile {profile_index}] Starting Save the Life automation script")
        print(f"{'='*60}")

        driver = create_firefox_driver(profile_path)

        if not access_savethelife(driver, profile_index):
            return False

        if not login_and_checkin_savethelife(driver, profile_index):
            return False

        return True

    except Exception as e:
        print(f"[Profile {profile_index}] Unexpected error: {str(e)}")
        return False

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

if __name__ == "__main__":
    # run_savethelife_script(FIREFOX_PROFILES[1], 2)  # Test run with first profile
    results = run_all_batches(run_savethelife_script, FIREFOX_PROFILES)

    # Thống kê kết quả
    total = len(results)
    success = sum(1 for r in results if r)
    print(f"\n{'='*60}")
    print(f"KẾT QUẢ TỔNG KẾT")
    print(f"{'='*60}")
    print(f"Tổng profiles: {total}")
    print(f"Thành công:    {success}")
    print(f"Thất bại:      {total - success}")
    print(f"{'='*60}")
