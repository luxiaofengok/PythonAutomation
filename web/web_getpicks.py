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
PICKS_URL = "https://go.getpicks.app/"

# ========================================================
def access_picks(driver, profile_index):
    """Step P1: Access https://go.getpicks.app/"""
    try:
        print(f"[Profile {profile_index}] [P1] Accessing {PICKS_URL}...")
        driver.get(PICKS_URL)

        # Wait for page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)

        print(f"[Profile {profile_index}] [P1] Page loaded successfully")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] [P1] Error accessing page: {str(e)}")
        return False

def click_login_and_google_picks(driver, profile_index):
    """Step P2: Click login button, then login with Google (handle popup)"""
    print(f"[Profile {profile_index}] [P2] Starting login process...")

    # Find and click login button
    login_selectors = [
        "/html/body/div[1]/div/button",
        "//button[contains(., 'Sign in')]",
    ]
    login_clicked = find_element_by_selectors(driver, login_selectors, 5)
    if not login_clicked:
        print(f"[Profile {profile_index}] [P2] Failed to click login button")
        return False
    click_element_safe(driver, login_clicked)

    confirm_selectors = [
        "//*[@id='radix-:r6:']/div[4]/div[1]/div[2]/button[1]",
        "//button[contains(., 'Log in')]",
    ]
    confirm_button = find_element_by_selectors(driver, confirm_selectors, 10)
    if confirm_button:
        click_element_safe(driver, confirm_button)

    time.sleep(5)
    # Handle Google login popup
    login_with_google(driver, profile_index)
    time.sleep(15)  # Wait for login to complete
    return True

def check_in_picks(driver, profile_index):
    """Step P3: Check if login was successful by looking for a specific element"""

    claim_selectors = [
        "/html/body/div[1]/main/div/div[1]/div/div/div[1]/button",
        "//button[contains(., 'Claim')]",
    ]
    claim_button = find_element_by_selectors(driver, claim_selectors, 10)
    if claim_button:
        click_element_safe(driver, claim_button)
        time.sleep(5)  # Wait for any post-login actions to complete
    
    generate_selectors = [
        "/html/body/div[1]/main/div/div[1]/button/div[2]/div[2]/span[1]",
        "//span[contains(., 'Generate')]",
    ]
    generate_button = find_element_by_selectors(driver, generate_selectors, 10)
    if not generate_button:
        print(f"[Profile {profile_index}] [P3] Login check failed - 'Generate' button not found")
        return False
    click_element_safe(driver, generate_button)
    time.sleep(5)  # Wait for any post-login actions to complete

    reveall_selectors = [
        "//*[@id='radix-:r0:']/div/div/div[3]/button/span",
        "//span[contains(., 'Reveal')]",
    ]
    reveall_button = find_element_by_selectors(driver, reveall_selectors, 10)
    if not reveall_button:
        print(f"[Profile {profile_index}] [P3] Login check failed - 'Reveal' button not found")
        return False
    click_element_safe(driver, reveall_button)
    time.sleep(5)  # Wait for any post-login actions to complete
    main_window = driver.current_window_handle

    share_selectors = [
        "//*[@id='radix-:r0:']/div/div/div[4]/button/span",
        "//span[contains(., 'Share to play')]",
    ]
    share_button = find_element_by_selectors(driver, share_selectors, 10)

    if not share_button:
        print(f"[Profile {profile_index}] [P3] Login check failed - 'Share to play' button not found")
        return False
    click_element_safe(driver, share_button)
    time.sleep(2)
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            time.sleep(2)
            driver.close()

    driver.switch_to.window(main_window)
    time.sleep(15)  # Wait for any post-login actions to complete
    return True

def run_picks_script(profile_path, profile_index):
    """Run the full Picks automation script for a given profile"""
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"[Profile {profile_index}] Starting GetPicks automation script")
        print(f"{'='*60}")

        driver = create_firefox_driver(profile_path)
        if not access_picks(driver, profile_index):
            return False

        if not click_login_and_google_picks(driver, profile_index):
            return False

        if not check_in_picks(driver, profile_index):
            return False

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
    # run_picks_script(FIREFOX_PROFILES[0], 1)
    results = run_all_batches(run_picks_script, FIREFOX_PROFILES)
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



