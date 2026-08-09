from web_source import (
    create_firefox_driver,
    check_and_login,
    login_with_google,
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
COURTYARD_URL = "https://courtyard.io/rewards"

# ========================================================

def access_courtyard(driver, profile_index):
    """Step C1: Access https://courtyard.io/rewards"""
    try:
        print(f"[Profile {profile_index}] [C1] Accessing {COURTYARD_URL}...")
        driver.get(COURTYARD_URL)

        # Wait for page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)

        print(f"[Profile {profile_index}] [C1] Page loaded successfully")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] [C1] Error accessing page: {str(e)}")
        return False
    
def click_login_and_google(driver, profile_index):
    """Step C2: Click login button, then login with Google (handle popup)"""
    print(f"[Profile {profile_index}] [C2] Starting login process...")

    # Find and click login button
    login_selectors = [

        "/html/body/div[4]/div/div/main/div/div[2]/div/button[1]",
        "//button[contains(., 'Log in')]"
    ]
    login_clicked = find_element_by_selectors(driver, login_selectors, 5)
    if not login_clicked:
        print(f"[Profile {profile_index}] [C2] Failed to click login button")
        return False
    click_element_safe(driver, login_clicked)

    time.sleep(2)
    # Handle Google login popup
    login_with_google(driver, profile_index)
    time.sleep(10)  # Wait for login to complete
    return True

    

def checkin_courtyard(driver, profile_index):
    """Step C3: Click Check-in button if available"""
    print(f"[Profile {profile_index}] [C3] Checking for Check-in button...")
    checkin_selectors = [
        "/html/body/div[4]/div/div/main/div/div[2]/div[1]/div[2]/button[1]",
        "/html/body/div[4]/div/div/main/div/div[2]/div[1]/div[2]/button[1]/span[1]",
        "//span[contains(., 'Roll Daily Points')]",
        "//button[contains(., 'Roll Daily Points')]",
    ]
    checkin_button = find_element_by_selectors(driver, checkin_selectors, 5)
    if not checkin_button:
        print(f"[Profile {profile_index}] [C3] Check-in button not found or already checked in")
        return False  # Không phải lỗi nếu không tìm thấy, có thể đã check-in rồi
    click_element_safe(driver, checkin_button)
    time.sleep(2)
    Stop_roll_selectors = [
    # Dùng class đặc trưng - chính xác nhất
    "//button[contains(@class,'MuiButton-containedError')]",
    "//button[contains(@class,'css-y3xisr')]",
    # Hoặc tìm theo text trực tiếp
    "//button[normalize-space()='Stop']",
    ]
    stop_roll_button = find_element_by_selectors(driver, Stop_roll_selectors, 5)
    if not stop_roll_button:
        print(f"[Profile {profile_index}] [C3] Stop roll button not found")
        return False    
    click_element_safe(driver, stop_roll_button)
    time.sleep(5)
    print(f"[Profile {profile_index}] [C3] Check-in completed successfully")
    return True

def run_courtyard_script(profile_path, profile_index):
    """Run the full Courtyard automation script for a given profile"""
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"[Profile {profile_index}] Starting Courtyard automation script")
        print(f"{'='*60}")

        driver = create_firefox_driver(profile_path)

        if not access_courtyard(driver, profile_index):
            return False

        if not click_login_and_google(driver, profile_index):
            return False

        if not checkin_courtyard(driver, profile_index):
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
    # run_courtyard_script(FIREFOX_PROFILES[0], 1)  # Test run with first profile
    results = run_all_batches(run_courtyard_script, FIREFOX_PROFILES)

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


