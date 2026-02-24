
"""
Pip World Automation Script
Website: https://mm.pip.world/
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.web_source import (
    create_firefox_driver,
    find_element_by_selectors,
    click_element_safe,
    run_all_batches,
    cleanup_all,
    FIREFOX_PROFILES
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random

# ==================== TIMING CONFIGURATION ====================
WAIT_PAGE_LOAD = 30         # Chờ sau khi load trang
WAIT_AFTER_LOGIN = 30       # Chờ sau khi login để page load đầy đủ
WAIT_GOOGLE_LOGIN = 5       # Chờ sau khi click Google login
WAIT_ACCOUNT_SELECT = 3     # Chờ sau khi chọn tài khoản
WAIT_AFTER_BUTTON_CLICK = 3 # Chờ sau khi nhấn button
WAIT_BEFORE_CHECKIN = 3     # Chờ trước khi check in
WAIT_AFTER_CHECKIN = 6      # Chờ sau khi check in
WAIT_BEFORE_SHARE = 6       # Chờ trước khi share
WAIT_AFTER_SHARE = 60       # Chờ sau khi share (1 phút)
WAIT_BEFORE_CLAIM = 3       # Chờ trước khi claim
WAIT_AFTER_CLAIM = 5        # Chờ sau khi claim
WAIT_BEFORE_CLOSE = 5       # Chờ trước khi đóng browser
ELEMENT_TIMEOUT = 40        # Timeout tìm element (giây)
MAX_RETRIES = 3             # Số lần thử lại khi không tìm thấy element
# ============================================================

URL = "https://mm.pip.world/"


def reload_page_human_like(driver, profile_index, wait_min=25, wait_max=35):
    """Reload page with human-like behavior"""
    try:
        print(f"[Profile {profile_index}] Reloading page with human-like behavior...")

        # Scroll randomly before reload (human behavior)
        scroll_amount = random.randint(-200, 200)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(random.uniform(0.5, 1.2))

        # Move mouse randomly (simulate human movement)
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            actions = ActionChains(driver)
            actions.move_to_element_with_offset(body, random.randint(50, 300), random.randint(50, 300))
            actions.perform()
            time.sleep(random.uniform(0.3, 0.7))
        except:
            pass

        # Reload
        driver.refresh()

        # Random wait after reload
        wait_time = random.uniform(wait_min, wait_max)
        print(f"[Profile {profile_index}] Waiting {wait_time:.1f}s for page to reload...")
        time.sleep(wait_time)

        # Scroll to top naturally after reload
        driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
        time.sleep(random.uniform(0.5, 1.0))

        print(f"[Profile {profile_index}] Page reloaded successfully")

    except Exception as e:
        print(f"[Profile {profile_index}] Reload error: {str(e)}, trying simple refresh...")
        driver.refresh()
        time.sleep(wait_min)


def login_google_direct(driver, profile_index):
    """Login trực tiếp bằng Google không check login trước"""
    try:
        print(f"[Profile {profile_index}] Finding Google login button...")
        
        # Tìm button Google login theo xpath chính xác
        google_xpath = "/html/body/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div[1]/img"
        
        try:
            google_button = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, google_xpath))
            )
        except:
            # Fallback selectors nếu xpath chính không work
            print(f"[Profile {profile_index}] Trying alternative selectors...")
            google_selectors = [
                "/html/body/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]/div",
                "/html/body/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]",
                "//img[contains(@alt, 'Google')]",
                "//div[contains(@class, 'google')]",
                "//*[contains(text(), 'Google')]//ancestor::div[contains(@role, 'button') or @onclick]"
            ]
            google_button = find_element_by_selectors(driver, google_selectors, ELEMENT_TIMEOUT)
        
        if not google_button:
            print(f"[Profile {profile_index}] Google button not found!")
            return False
        
        driver.execute_script("arguments[0].scrollIntoView(true);", google_button)
        time.sleep(1)
        
        # Click vào element (có thể là img hoặc parent div)
        if not click_element_safe(driver, google_button):
            # Thử click parent element nếu click img không được
            try:
                parent = google_button.find_element(By.XPATH, "..")
                click_element_safe(driver, parent)
            except:
                pass
        
        print(f"[Profile {profile_index}] Clicked Google login button")
        time.sleep(WAIT_GOOGLE_LOGIN)
        
        # Chọn tài khoản Google
        account_selectors = [
            "//li[1]//div[@role='link']",
            "//div[@data-authuser='0']",
            "//ul//li[1]//div[contains(@class, 'BHzsHc')]",
            "(//div[contains(@jsname, 'V67aGc')])[1]"
        ]
        
        google_account = find_element_by_selectors(driver, account_selectors, 5)
        if google_account:
            google_account.click()
            print(f"[Profile {profile_index}] Selected Google account")
            time.sleep(WAIT_ACCOUNT_SELECT)
        
        # Nhấn Continue nếu có
        continue_selectors = [
            "//button[contains(., 'Continue')]",
            "//button[contains(., 'Tiếp tục')]"
        ]
        continue_button = find_element_by_selectors(driver, continue_selectors, 3)
        if continue_button:
            continue_button.click()
            print(f"[Profile {profile_index}] Clicked Continue")
            time.sleep(WAIT_AFTER_LOGIN)
        
        print(f"[Profile {profile_index}] Login completed successfully")
        return True
        
    except Exception as e:
        print(f"[Profile {profile_index}] Login error: {str(e)}")
        return False


def hover_element(driver, xpath, element_name, profile_index, wait_after=2, retries=MAX_RETRIES):
    """Hover vào element bằng ActionChains"""
    for attempt in range(retries):
        try:
            if attempt > 0:
                print(f"[Profile {profile_index}] Retry {attempt}/{retries-1} for hovering {element_name}...")
                time.sleep(2)
            
            print(f"[Profile {profile_index}] Finding {element_name} to hover...")
            
            # Wait for element
            element = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            
            # Scroll to element
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(1)
            
            # Hover using ActionChains
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            
            print(f"[Profile {profile_index}] Hovered on {element_name} successfully")
            time.sleep(wait_after)
            return True
            
        except Exception as e:
            if attempt < retries - 1:
                print(f"[Profile {profile_index}] Hover attempt {attempt+1} failed: {str(e)[:100]}")
                continue
            else:
                print(f"[Profile {profile_index}] Error hovering {element_name} after {retries} attempts: {str(e)}")
                return False
    
    return False


def click_button_by_xpath(driver, xpath, button_name, profile_index, wait_after=2, retries=MAX_RETRIES):
    """Click button bằng xpath với retry logic"""
    for attempt in range(retries):
        try:
            if attempt > 0:
                print(f"[Profile {profile_index}] Retry {attempt}/{retries-1} for {button_name}...")
                time.sleep(2)
            
            print(f"[Profile {profile_index}] Finding {button_name} button...")
            
            # Wait for element to be clickable
            button = WebDriverWait(driver, ELEMENT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            
            # Scroll to element
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
            time.sleep(1)
            
            # Highlight element (for debugging)
            driver.execute_script("arguments[0].style.border='3px solid red'", button)
            time.sleep(0.5)
            
            # Click
            if not click_element_safe(driver, button):
                if attempt < retries - 1:
                    continue
                print(f"[Profile {profile_index}] Failed to click {button_name}")
                return False
            
            print(f"[Profile {profile_index}] Clicked {button_name} successfully")
            time.sleep(wait_after)
            return True
            
        except Exception as e:
            if attempt < retries - 1:
                print(f"[Profile {profile_index}] Attempt {attempt+1} failed: {str(e)[:100]}")
                continue
            else:
                print(f"[Profile {profile_index}] Error clicking {button_name} after {retries} attempts: {str(e)}")
                return False
    
    return False


def process_profile(profile_path, profile_index):
    """Process một profile"""
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"[Profile {profile_index}] Starting...")
        print(f"{'='*60}\n")
        
        # Tạo driver
        driver = create_firefox_driver(profile_path)
        
        # Mở trang
        print(f"[Profile {profile_index}] Opening {URL}")
        driver.get(URL)
        time.sleep(WAIT_PAGE_LOAD)
        
        # Check page sau khi mở - chỉ reload nếu trang trống hoặc bị blocked
        max_reload_attempts = 3
        for reload_attempt in range(max_reload_attempts):
            try:
                # Check xem page có bị trắng hoặc blocked không
                page_body = driver.find_element(By.TAG_NAME, "body").text
                page_html = driver.page_source.lower()
                
                # Chỉ reload nếu:
                # 1. Trang trống trơn (body text < 50 ký tự)
                # 2. Có chữ "blocked" trong page
                is_blank = len(page_body.strip()) < 50
                is_blocked = "blocked" in page_html
                
                if is_blank or is_blocked:
                    if reload_attempt < max_reload_attempts - 1:
                        if is_blank:
                            print(f"[Profile {profile_index}] Page is blank after opening, reloading... (attempt {reload_attempt+1}/{max_reload_attempts})")
                        else:
                            print(f"[Profile {profile_index}] Page is blocked after opening, reloading... (attempt {reload_attempt+1}/{max_reload_attempts})")
                        reload_page_human_like(driver, profile_index, wait_min=25, wait_max=35)
                        continue
                    else:
                        print(f"[Profile {profile_index}] Page still blank/blocked after {max_reload_attempts} attempts")
                        return False
                else:
                    print(f"[Profile {profile_index}] Page opened successfully, proceeding to login...")
                    break
                    
            except Exception as e:
                print(f"[Profile {profile_index}] Warning: Page check error: {str(e)[:100]}, continuing anyway...")
                break
        
        # Login trực tiếp bằng Google
        if not login_google_direct(driver, profile_index):
            print(f"[Profile {profile_index}] Login failed!")
            return False
        
        # Wait for page to fully load after login
        print(f"[Profile {profile_index}] Waiting for page to load completely...")
        time.sleep(WAIT_AFTER_LOGIN)
        
        # Check page - chỉ reload nếu trang trống hoặc bị blocked
        max_reload_attempts = 3
        for reload_attempt in range(max_reload_attempts):
            try:
                # Check xem page có bị trắng hoặc blocked không
                page_body = driver.find_element(By.TAG_NAME, "body").text
                page_html = driver.page_source.lower()
                
                # Chỉ reload nếu:
                # 1. Trang trống trơn (body text < 50 ký tự)
                # 2. Có chữ "blocked" trong page
                is_blank = len(page_body.strip()) < 50
                is_blocked = "blocked" in page_html
                
                if is_blank or is_blocked:
                    if reload_attempt < max_reload_attempts - 1:
                        if is_blank:
                            print(f"[Profile {profile_index}] Page is blank, reloading... (attempt {reload_attempt+1}/{max_reload_attempts})")
                        else:
                            print(f"[Profile {profile_index}] Page is blocked, reloading... (attempt {reload_attempt+1}/{max_reload_attempts})")
                        reload_page_human_like(driver, profile_index, wait_min=25, wait_max=35)
                        continue
                    else:
                        print(f"[Profile {profile_index}] Page still blank/blocked after {max_reload_attempts} attempts")
                        return False
                else:
                    print(f"[Profile {profile_index}] Page loaded successfully, proceeding to tasks...")
                    break
                    
            except Exception as e:
                print(f"[Profile {profile_index}] Warning: Page check error: {str(e)[:100]}, continuing anyway...")
                break
        
        # XPath definitions
        xpath_dropdown = "/html/body/div[1]/div[1]/div[1]/div[3]/div[2]"
        
        # B1: CLICK vào dropdown để mở menu (không phải hover)
        if not click_button_by_xpath(driver, xpath_dropdown, "Dropdown (open menu)", profile_index, 3):
            print(f"[Profile {profile_index}] Failed to click dropdown")
            return False
        
        print(f"[Profile {profile_index}] Dropdown opened, waiting for menu to appear...")
        time.sleep(2)
        
        # B2: Tìm và click button Check In (sau khi dropdown mở)
        # Chỉ thử 1 lần với timeout ngắn, không thấy thì bỏ qua
        checkin_selectors = [
            "//button[contains(text(), 'CHECK IN')]",
            "//button[normalize-space()='CHECK IN']"
        ]
        
        checkin_found = False
        for selector in checkin_selectors:
            try:
                # Timeout ngắn 5s, retries=1 - tìm nhanh thôi
                button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                time.sleep(0.5)
                if click_element_safe(driver, button):
                    print(f"[Profile {profile_index}] Clicked Check In successfully")
                    time.sleep(WAIT_AFTER_CHECKIN)
                    checkin_found = True
                    break
            except:
                continue
        
        if not checkin_found:
            print(f"[Profile {profile_index}] Check In not found - already checked in, skipping...")
        
        # B3: Click button Share (menu vẫn đang mở)
        share_selectors = [
            "//button[contains(text(), 'SHARE')]",
            "//button[contains(text(), 'Share')]",
            "//button[contains(text(), 'share')]",
            "//button[contains(., 'Share')]",
            "//button[contains(@class, 'share')]",
            "//*[contains(text(), 'SHARE')]//ancestor::button",
            "//button[normalize-space()='SHARE']"
        ]
        
        share_found = False
        for selector in share_selectors:
            try:
                if click_button_by_xpath(driver, selector, "Share", profile_index, WAIT_AFTER_BUTTON_CLICK):
                    share_found = True
                    break
            except:
                continue
        
        if not share_found:
            print(f"[Profile {profile_index}] Share button not found - might be already shared, continuing...")
        
        # B4: Click lại vào dropdown ngay sau khi share
        if not click_button_by_xpath(driver, xpath_dropdown, "Dropdown (2nd time - open menu)", profile_index, 3):
            print(f"[Profile {profile_index}] Failed to click dropdown (2nd time)")
            return False
        
        print(f"[Profile {profile_index}] Dropdown opened again, waiting for menu...")
        time.sleep(2)
        
        # B5: Đợi 1 phút trước khi claim
        print(f"[Profile {profile_index}] Waiting {WAIT_AFTER_SHARE}s before Claim...")
        time.sleep(WAIT_AFTER_SHARE)
        
        # B6: Click button Claim
        claim_selectors = [
            "//button[contains(text(), 'CLAIM')]",
            "//button[contains(text(), 'Claim')]",
            "//button[contains(text(), 'claim')]",
            "//button[contains(., 'Claim')]",
            "//button[contains(@class, 'claim')]",
            "//*[contains(text(), 'CLAIM')]//ancestor::button",
            "//button[normalize-space()='CLAIM']"
        ]
        
        claim_found = False
        for selector in claim_selectors:
            try:
                if click_button_by_xpath(driver, selector, "Claim", profile_index, WAIT_AFTER_CLAIM):
                    claim_found = True
                    break
            except:
                continue
        
        if not claim_found:
            print(f"[Profile {profile_index}] Claim button not found - might be already claimed, continuing...")
        
        print(f"[Profile {profile_index}] ✅ All tasks completed successfully!")
        time.sleep(WAIT_BEFORE_CLOSE)
        
        return True
        
    except Exception as e:
        print(f"[Profile {profile_index}] ❌ Error: {str(e)}")
        return False
        
    finally:
        if driver:
            try:
                driver.quit()
                print(f"[Profile {profile_index}] Browser closed")
            except:
                pass
        
        # Cleanup
        cleanup_all(profile_path, profile_index)


def main():
    """Main function - chạy tất cả profiles"""
    print("\n" + "="*60)
    print("PIP WORLD AUTOMATION")
    print("="*60 + "\n")
    
    # Chạy tất cả 3 batches
    results = run_all_batches(process_profile)
    
    # Summary
    success_count = sum(1 for r in results if r)
    total_count = len(results)
    
    print("\n" + "="*60)
    print(f"SUMMARY: {success_count}/{total_count} profiles completed successfully")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()