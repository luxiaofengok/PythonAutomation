"""Web Automation Framework - Common utilities for browser automation"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor, as_completed
import time, os, shutil, tempfile, glob, subprocess

FIREFOX_PROFILES = [
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\EYFYwuoC.Profile 1",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\K7Ms67Yf.Hồ sơ 2",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\jmCZhbq0.Hồ sơ 3",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\hVlpgpyW.Hồ sơ 4",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\EYUavWHf.Hồ sơ 5",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\gA6pOEMK.Hồ sơ 6",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\rPhWDpKS.Hồ sơ 7",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\BGU2Szlj.Hồ sơ 8",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\9bThzlN5.Hồ sơ 9",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\1o3VePEW.Hồ sơ 10",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\wt1JsR72.Hồ sơ 11",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\r2LAx6mT.Hồ sơ 12",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\XNaxUADk.Hồ sơ 13",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\edPXdFYz.Hồ sơ 14",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\91PbC0aX.Hồ sơ 15",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kxLMQ7uV.Hồ sơ 16",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\j09dZ5W6.Hồ sơ 17",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\VrxQR82t.Hồ sơ 18",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\WVZoasKN.Hồ sơ 19",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\Y2YfF82j.Hồ sơ 20",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\fLKSCXiH.Hồ sơ 21",
    "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\8LrfqVIk.Hồ sơ 22",
]

def create_firefox_driver(profile_path, optimize=True):
    """Create Firefox driver with optimization settings"""
    options = Options()
    options.profile = profile_path
    
    if optimize:
        prefs = {
            "browser.cache.disk.enable": False,
            "browser.cache.memory.enable": True,
            "browser.cache.offline.enable": False,
            "browser.sessionstore.resume_from_crash": False,
            "browser.cache.disk.capacity": 0,
            "browser.cache.disk.smart_size.enabled": False
        }
        for key, value in prefs.items():
            options.set_preference(key, value)
    
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    return driver


def find_element_by_selectors(driver, selectors, wait_time=5):
    """Find element using multiple selectors"""
    for selector in selectors:
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, selector))
            )
            if element.is_displayed():
                return element
        except:
            continue
    return None


def click_element_safe(driver, element):
    """Click element using multiple methods"""
    methods = [
        lambda: driver.execute_script("arguments[0].click();", element),
        lambda: ActionChains(driver).move_to_element(element).pause(1).click().perform(),
        lambda: element.click()
    ]
    
    for method in methods:
        try:
            method()
            return True
        except:
            continue
    return False


def check_login_status(driver, logged_in_indicators, profile_index=0):
    """Check if already logged in"""
    for indicator in logged_in_indicators:
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, indicator))
            )
            print(f"[Profile {profile_index}] Already logged in")
            return True
        except:
            continue
    return False


def login_with_google(driver, profile_index=0):
    """Perform Google login flow"""
    try:
        # Find and click Google button
        google_selectors = [
            "//button[contains(., 'Continue with Google')]",
            "//button[contains(., 'Google')]",
            "//button[contains(., 'Sign in with Google')]",
            "//*[contains(@class, 'google')]//button",
            "//button[.//text()[contains(., 'Google')]]"
        ]
        
        google_button = find_element_by_selectors(driver, google_selectors)
        if not google_button:
            return False
        
        driver.execute_script("arguments[0].scrollIntoView(true);", google_button)
        time.sleep(1)
        google_button.click()
        time.sleep(5)
        
        # Select Google account
        account_selectors = [
            "//li[1]//div[@role='link']",
            "//div[@data-authuser='0']",
            "//ul//li[1]//div[contains(@class, 'BHzsHc')]",
            "(//div[contains(@jsname, 'V67aGc')])[1]"
        ]
        
        google_account = find_element_by_selectors(driver, account_selectors, 5)
        if google_account:
            google_account.click()
            time.sleep(3)
        
        # Click continue if present
        continue_selectors = [
            "//button[contains(., 'Continue')]",
            "//button[contains(., 'Tiếp tục')]"
        ]
        continue_button = find_element_by_selectors(driver, continue_selectors, 3)
        if continue_button:
            continue_button.click()
            time.sleep(3)
        
        print(f"[Profile {profile_index}] Login completed")
        return True
        
    except Exception as e:
        print(f"[Profile {profile_index}] Login error: {str(e)}")
        return False


def check_and_login(driver, logged_in_indicators, profile_index=0):
    """Check login status and login if needed"""
    if check_login_status(driver, logged_in_indicators, profile_index):
        return True
    return login_with_google(driver, profile_index)


def clean_temp_files(profile_index=0):
    """Clean temporary files to free disk space"""
    try:
        temp_dir = tempfile.gettempdir()
        patterns = ["tmp*.tmp", "*.tmp", "rust_mozprofile*", "firefox_*", "tmpaddon*", "webdriver-py-*", "tmp*"]
        
        removed, failed = 0, 0
        for pattern in patterns:
            for path in glob.glob(os.path.join(temp_dir, pattern)):
                try:
                    if time.time() - os.path.getmtime(path) > 60:
                        if os.path.isfile(path):
                            os.remove(path)
                        else:
                            shutil.rmtree(path, ignore_errors=True)
                        removed += 1
                except:
                    failed += 1
        
        print(f"[Profile {profile_index}] Cleaned {removed} items, {failed} in use")
        
        # PowerShell cleanup for old files
        try:
            ps_cmd = f'Get-ChildItem -Path "{temp_dir}" -Filter "tmp*" -File | Where-Object {{$_.LastWriteTime -lt (Get-Date).AddDays(-1)}} | Remove-Item -Force -ErrorAction SilentlyContinue'
            subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, timeout=10)
        except:
            pass
    except Exception as e:
        print(f"[Profile {profile_index}] Cleanup error: {str(e)}")


def clean_profile_cache(profile_path):
    """Clean Firefox profile cache"""
    for folder in ["cache2", "thumbnails", "OfflineCache", "startupCache", "shader-cache"]:
        try:
            shutil.rmtree(os.path.join(profile_path, folder), ignore_errors=True)
        except:
            pass


def cleanup_all(profile_path=None, profile_index=0):
    """Complete cleanup of temp files and profile cache"""
    clean_temp_files(profile_index)
    if profile_path:
        clean_profile_cache(profile_path)


def click_at_position(driver, x_percent, y_percent):
    """Click at specific screen position"""
    try:
        w = driver.execute_script("return window.innerWidth;")
        h = driver.execute_script("return window.innerHeight;")
        x, y = int(w * x_percent), int(h * y_percent)
        
        actions = ActionChains(driver)
        actions.move_by_offset(x, y).click().perform()
        time.sleep(1)
        actions.move_by_offset(-x, -y).perform()
    except Exception as e:
        print(f"Click position error: {str(e)}")


def run_batch(profiles, batch_num, task_function, max_workers=8):
    """
    Run batch of profiles concurrently
    Args:
        profiles: List of (profile_path, profile_index) tuples
        batch_num: Batch number for logging
        task_function: Function to run for each profile (profile_path, profile_idx)
        max_workers: Number of concurrent workers
    """
    print(f"\n{'='*60}\nBatch {batch_num} - {len(profiles)} profiles\n{'='*60}\n")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(task_function, p[0], p[1]): p for p in profiles}
        results = [future.result() for future in as_completed(futures)]
    
    print(f"\n{'='*60}\nBatch {batch_num} completed\n{'='*60}\n")
    
    # Cleanup after batch
    clean_temp_files()
    
    return results


def run_all_batches(task_function, profiles=None, wait_between_batches=10):
    """
    Run all 3 batches (8+8+6 profiles)
    Args:
        task_function: Function to run for each profile
        profiles: List of profile paths (uses FIREFOX_PROFILES if None)
        wait_between_batches: Seconds to wait between batches
    """
    if profiles is None:
        profiles = FIREFOX_PROFILES
    
    batches = [
        [(profiles[i], i+1) for i in range(8)],
        [(profiles[i], i+1) for i in range(8, 16)],
        [(profiles[i], i+1) for i in range(16, min(22, len(profiles)))]
    ]
    
    all_results = []
    for i, batch in enumerate(batches, 1):
        all_results.extend(run_batch(batch, i, task_function, max_workers=8 if i < 3 else 6))
        
        if i < len(batches):
            print(f"\nWaiting {wait_between_batches} seconds before next batch...\n")
            time.sleep(wait_between_batches)
    
    # Final cleanup
    print("\n[Final Cleanup] Cleaning up...")
    clean_temp_files()
    print("[Final Cleanup] Done!")
    
    return all_results

# Quick usage examples
if __name__ == "__main__":
    print("Web Automation Framework")
    print("=" * 60)
    print("Core Functions:")
    print("- create_firefox_driver, check_and_login")
    print("- find_element_by_selectors, click_element_safe")
    print("- clean_temp_files, cleanup_all")
    print("\nBatch Functions:")
    print("- run_batch(profiles, batch_num, task_function, max_workers=8)")
    print("- run_all_batches(task_function, profiles=None)")
    print("=" * 60)
