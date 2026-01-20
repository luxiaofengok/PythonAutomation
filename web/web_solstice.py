from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import cleanup functions
from web_source import clean_temp_files, clean_profile_cache

TARGET_URL = "https://app.megaphone.xyz/pages/solstice?r=mxhpvIHL1Glq"

FIREFOX_PROFILES = [
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\EYFYwuoC.Profile 1",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\K7Ms67Yf.Hồ sơ 2",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\jmCZhbq0.Hồ sơ 3",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\hVlpgpyW.Hồ sơ 4",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\EYUavWHf.Hồ sơ 5",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\gA6pOEMK.Hồ sơ 6",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\rPhWDpKS.Hồ sơ 7",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\BGU2Szlj.Hồ sơ 8",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\9bThzlN5.Hồ sơ 9",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\1o3VePEW.Hồ sơ 10",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\wt1JsR72.Hồ sơ 11",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\r2LAx6mT.Hồ sơ 12",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\XNaxUADk.Hồ sơ 13",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\edPXdFYz.Hồ sơ 14",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\91PbC0aX.Hồ sơ 15",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\kxLMQ7uV.Hồ sơ 16",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\j09dZ5W6.Hồ sơ 17",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\VrxQR82t.Hồ sơ 18",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\WVZoasKN.Hồ sơ 19",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\Y2YfF82j.Hồ sơ 20",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\fLKSCXiH.Hồ sơ 21",
    r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles\8LrfqVIk.Hồ sơ 22",
]

def find_and_click(driver, selectors, timeout=30, scroll=True):
    """Helper function to find and click element with multiple selectors"""
    for selector in selectors:
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            if scroll:
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
            element.click()
            return True
        except:
            continue
    return False

def login_with_google(driver, profile_idx):
    """Handle Google login process"""
    try:
        # Check if login button exists
        login_selectors = [
            "//button[contains(translate(., 'LOGIN', 'login'), 'login')]",
            "//button[contains(., 'Sign in')]",
            "//button[contains(., 'Connect')]",
            "//*[contains(text(), 'Login') or contains(text(), 'Sign in')]"
        ]
        
        if not find_and_click(driver, login_selectors, timeout=5):
            print(f"[Profile {profile_idx}] Already logged in or login button not found")
            return True
        
        print(f"[Profile {profile_idx}] Clicked login button")
        time.sleep(3)
        
        # Click Google login button
        google_selectors = [
            "//button[contains(., 'Continue with Google')]",
            "//button[contains(., 'Google')]",
            "//button[contains(., 'Sign in with Google')]",
            "//*[contains(@class, 'google')]//button",
            "//div[contains(., 'Google')]/parent::button"
        ]
        
        if not find_and_click(driver, google_selectors, timeout=5):
            print(f"[Profile {profile_idx}] Google login button not found")
            return False
        
        print(f"[Profile {profile_idx}] Clicked Google login")
        time.sleep(5)
        
        # Select Google account
        account_selectors = [
            "//li[1]//div[@role='link']",
            "//div[@data-authuser='0']",
            "(//div[contains(@jsname, 'V67aGc')])[1]",
            "//ul//li[1]//div[contains(@class, 'BHzsHc')]"
        ]
        
        if find_and_click(driver, account_selectors, timeout=5, scroll=False):
            print(f"[Profile {profile_idx}] Selected Google account")
            time.sleep(3)
        
        # Click continue if needed
        continue_selectors = [
            "//button[contains(., 'Continue')]",
            "//button[contains(., 'Tiếp tục')]"
        ]
        find_and_click(driver, continue_selectors, timeout=3, scroll=False)
        
        print(f"[Profile {profile_idx}] Login completed")
        return True
        
    except Exception as e:
        print(f"[Profile {profile_idx}] Login error: {str(e)}")
        return False

def click_checkin(driver, profile_idx):
    """Click on check-in button"""
    try:
        time.sleep(5)
        
        # Click check-in button
        checkin_selectors = [
            "/html/body/div[1]/main/div/div[2]/div[3]/div[1]/span",
            "//span[contains(., 'Check')]",
            "//span[contains(., 'check')]",
            "//button[contains(., 'Check')]"
        ]
        
        if find_and_click(driver, checkin_selectors, timeout=10):
            print(f"[Profile {profile_idx}] Check-in clicked successfully")
            time.sleep(2)
            return True
        else:
            print(f"[Profile {profile_idx}] Check-in button not found")
            return False
            
    except Exception as e:
        print(f"[Profile {profile_idx}] Check-in error: {str(e)}")
        return False

def access_website_with_profile(profile_path, profile_idx):
    """Main function to access website with profile"""
    driver = None
    try:
        print(f"[Profile {profile_idx}] Starting...")
        
        options = Options()
        options.profile = profile_path
        
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        driver.get(TARGET_URL)
        print(f"[Profile {profile_idx}] Page loaded")
        
        time.sleep(5)
        
        # Login with Google
        login_with_google(driver, profile_idx)
        
        # Wait for page to stabilize after login
        time.sleep(5)
        
        # Click check-in
        click_checkin(driver, profile_idx)
        
        # Wait before closing
        print(f"[Profile {profile_idx}] Waiting before closing...")
        time.sleep(10)
        
        return f"Profile {profile_idx}: Success"
        
    except Exception as e:
        print(f"[Profile {profile_idx}] Error: {str(e)}")
        return f"Profile {profile_idx}: Failed - {str(e)}"
        
    finally:
        if driver:
            driver.quit()
            print(f"[Profile {profile_idx}] Closed")
        
        # Cleanup profile cache
        try:
            clean_profile_cache(profile_path)
        except:
            pass

def run_batch(profiles, batch_num, max_workers=8):
    """Run batch of profiles"""
    print(f"\n{'='*60}\nBatch {batch_num} - {len(profiles)} profiles\n{'='*60}\n")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(access_website_with_profile, p[0], p[1]): p for p in profiles}
        results = [future.result() for future in as_completed(futures)]
    
    print(f"\n{'='*60}\nBatch {batch_num} completed\n{'='*60}\n")
    
    # Cleanup temp files
    clean_temp_files()
    
    return results

def main():
    print("="*60)
    print("Firefox Multi-Profile Automation - Solstice")
    print(f"URL: {TARGET_URL}")
    print(f"Total: {len(FIREFOX_PROFILES)} profiles in 3 batches (8+8+6)")
    print("="*60)
    
    batches = [
        [(FIREFOX_PROFILES[i], i+1) for i in range(8)],
        [(FIREFOX_PROFILES[i], i+1) for i in range(8, 16)],
        [(FIREFOX_PROFILES[i], i+1) for i in range(16, 22)]
    ]
    
    all_results = []
    for i, batch in enumerate(batches, 1):
        all_results.extend(run_batch(batch, i, max_workers=8 if i < 3 else 6))
        if i < len(batches):
            print(f"\nWaiting 10 seconds...\n")
            time.sleep(10)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for result in all_results:
        print(result)
    print("="*60)
    
    # Final cleanup
    print("\n[Final Cleanup] Cleaning up...")
    clean_temp_files()
    print("[Final Cleanup] Done!")

if __name__ == "__main__":
    main()
