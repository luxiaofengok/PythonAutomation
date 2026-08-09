from web_source import (
    create_firefox_driver,
    check_and_login,
    login_with_google,
    find_element_by_selectors,
    click_element_safe,
    FIREFOX_PROFILES,
    run_all_batches,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ==================== CONFIGURATION ====================
CARDIUM_URL = "https://beta.cardium.games/?ref=000zpgny"

# ========================================================
def access_cardium(driver, profile_index):
   
    try:
        print(f"[Profile {profile_index}] [N1] Accessing {CARDIUM_URL}...")
        driver.get(CARDIUM_URL)

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

def click_login_and_google_cardium(driver, profile_index):
    """Step N2: Click login button, then login with Google (handle popup)"""
    print(f"[Profile {profile_index}] [N2] Starting login process...")
    # Find and click login button
    login_selectors = [
        "//*[@id='top']/div[4]/div[1]/div[2]/a[2]",
        "//a[contains(., 'Dashboard')]",
    ]
    login_clicked = find_element_by_selectors(driver, login_selectors, 5)
    if not login_clicked:
        print(f"[Profile {profile_index}] [N2] Failed to click login button")
        return False
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_clicked)
    time.sleep(1)
    click_element_safe(driver, login_clicked)

    time.sleep(5)
    # Handle Google login popup
    login_with_google(driver, profile_index)
    time.sleep(30)  # Wait for login to complete

    return True

def check_in_cardium(driver, profile_index):
    check_in_selectors=[
        "/html/body/div[2]/main/div/div/section[1]/div[2]/button/span",
        "//span[contains(., 'Check in today ')]",
    ]
    check_in_button = find_element_by_selectors(driver,check_in_selectors,5)
    if check_in_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", check_in_button)
        time.sleep(1)
        click_element_safe(driver, check_in_button)
    time.sleep(2)

    open_x_selectors=[
        "/html/body/div[2]/main/div/section[3]/ul/li[1]/div[3]/button",
        "//button[constains(., 'Open X')]",
    ]
    open_x_button = find_element_by_selectors(driver,open_x_selectors,5)
    if open_x_button:
        main_window = driver.current_window_handle
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", open_x_button)
        time.sleep(1)
        click_element_safe(driver, open_x_button)
        time.sleep(1)
        for handle in driver.window_handles:
            if handle!= main_window:
                driver.switch_to.window(handle)
                break
        time.sleep(3)
        driver.close()
        time.sleep(2)
        driver.switch_to.window(main_window)
    time.sleep(3)

    open_post_selectors=[
        "/html/body/div[2]/main/div/section[3]/ul/li[2]/div[3]/button",
        "//button[constains(., 'Open post')]",
    ]
    open_post_button = find_element_by_selectors(driver,open_post_selectors,5)
    if open_post_button:
        main_window = driver.current_window_handle
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", open_post_button)
        time.sleep(1)
        click_element_safe(driver, open_post_button)
        time.sleep(1)
        for handle in driver.window_handles:
            if handle!= main_window:
                driver.switch_to.window(handle)
                break
        time.sleep(3)
        driver.close()
        time.sleep(2)
        driver.switch_to.window(main_window)
    time.sleep(60)
    return True

def run_cardium_script(profile_path, profile_index):
    """Chạy automation script cho CARDIUM"""
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"\n[Profile {profile_index}] Starting CARDIUM automation...")
        print(f"{'='*60}")
        driver = create_firefox_driver(profile_path)
        
        if not access_cardium(driver, profile_index):
            return False
        
        if not click_login_and_google_cardium(driver, profile_index):
            return False
        
        if not check_in_cardium(driver, profile_index):
            return False
        
        print(f"[Profile {profile_index}] CARDIUM automation completed successfully")
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
    # run_cardium_script(FIREFOX_PROFILES[6],7)

    results = run_all_batches(run_cardium_script, FIREFOX_PROFILES)
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




    

    