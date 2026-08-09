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
# ==================== CONFIGURATION ====================
GXT_URL = "https://gxtexchange.com/mining"

# ========================================================

def access_gxt(driver, profile_index):
    """Step N1: Access https://gxtexchange.com/mining"""
    try:
        print(f"[Profile {profile_index}] [N1] Accessing {GXT_URL}...")
        driver.get(GXT_URL)

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

def login_and_checkin_gxt(driver, profile_index):
    # Handle Google login popup
    login_with_google(driver, profile_index)
    time.sleep(15)  # Wait for login to complete

    mining_selectors = [
        "/html/body/div[1]/div/div[4]/div[1]/a[2]",
        "//a[contains(., 'Mining')]",
    ]
    mining_button = find_element_by_selectors(driver, mining_selectors, 10)
    if mining_button:
        scroll_to_element(driver, mining_button)
        click_element_safe(driver, mining_button)
        time.sleep(2)  # Wait for any post-login actions to complete

    Claim_selectors = [
        "/html/body/div[1]/div/div[3]/div[1]/button",
        "//button[contains(., 'Claim GXT')]",
    ]
    Claim_button = find_element_by_selectors(driver, Claim_selectors, 10)
    if Claim_button:
        scroll_to_element(driver, Claim_button)
        click_element_safe(driver, Claim_button)
        time.sleep(5)  # Wait for any post-login actions to complete

    return True

def run_gxt_script(profile_path, profile_index):
    """Chạy automation script cho GXT"""
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"\n[Profile {profile_index}] Starting GXT automation...")
        print(f"{'='*60}")
        driver = create_firefox_driver(profile_path)
        
        if not access_gxt(driver, profile_index):
            return False
        
        if not login_and_checkin_gxt(driver, profile_index):
            return False
        
        
        print(f"[Profile {profile_index}] GXT automation completed successfully")
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

    results = run_all_batches(run_gxt_script, FIREFOX_PROFILES)
    total = len(results)
    success = sum(1 for r in results if r)
    print(f"\n{'='*60}")
    print(f"KẾT QUẢ TỔNG KẾT")
    print(f"{'='*60}")
    print(f"Tổng profiles: {total}")
    print(f"Thành công:    {success}")
    print(f"Thất bại:      {total - success}")
    print(f"{'='*60}")