from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import cleanup functions
from web_source import clean_temp_files, clean_profile_cache

TARGET_URL = "https://waitlist.kindredlabs.ai/dashboard"

def random_delay(min_sec=1, max_sec=3):
    """Random delay to simulate human behavior"""
    time.sleep(random.uniform(min_sec, max_sec))

def human_like_scroll(driver):
    """Simulate human-like scrolling"""
    try:
        # Random scroll patterns
        scroll_amount = random.randint(100, 500)
        driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
        random_delay(1, 2)
        driver.execute_script("window.scrollTo(0, 0);")
        random_delay(0.5, 1.5)
    except:
        pass

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

def find_and_click(driver, selectors, timeout=5, scroll=True):
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
            "/html/body/nav/div/div/button/span",
            "//nav//button//span",
            "//button[contains(translate(., 'LOGIN', 'login'), 'login')]",
            "//button[contains(., 'Sign in')]",
            "//*[contains(text(), 'Login') or contains(text(), 'Sign in')]"
        ]
        
        if not find_and_click(driver, login_selectors, timeout=5):
            print(f"[Profile {profile_idx}] Already logged in or login button not found")
            return True
        
        print(f"[Profile {profile_idx}] Clicked login button")
        time.sleep(5)
        
        # Scroll to find and click Google login button (keep it in center of screen)
        google_selectors = [
            "/html/body/main/div[3]/div[2]/div[1]/div/div[2]/button[1]/img",
            "//button[1]//img[contains(@alt, 'Google') or contains(@src, 'google')]",
            "//img[contains(@alt, 'Google')]/parent::button"
        ]
        
        print(f"[Profile {profile_idx}] Scrolling to find Google login button...")
        google_button = None
        
        for selector in google_selectors:
            try:
                google_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                # Scroll element to center of viewport
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", google_button)
                time.sleep(1)
                print(f"[Profile {profile_idx}] Found and centered Google button")
                break
            except:
                continue
        
        if not google_button:
            print(f"[Profile {profile_idx}] Google login button not found")
            return False
        
        # Store current window handle before clicking
        original_window = driver.current_window_handle
        
        # Click the button
        try:
            google_button.click()
        except:
            driver.execute_script("arguments[0].click();", google_button)
        
        print(f"[Profile {profile_idx}] Clicked Google login button")
        time.sleep(5)
        
        # Wait for new window to open and switch to it
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        all_windows = driver.window_handles
        
        # Switch to the new window
        for window in all_windows:
            if window != original_window:
                driver.switch_to.window(window)
                print(f"[Profile {profile_idx}] Switched to Google login window")
                break
        
        time.sleep(5)
        
        # Select Google account
        account_selectors = [
            "//li[1]//div[@role='link']",
            "//div[@data-authuser='0']",
            "(//div[contains(@jsname, 'V67aGc')])[1]"
        ]
        
        if find_and_click(driver, account_selectors, timeout=5, scroll=False):
            print(f"[Profile {profile_idx}] Selected Google account")
            time.sleep(5)
        
        # Click continue if needed
        continue_selectors = ["//button[contains(., 'Continue')]"]
        find_and_click(driver, continue_selectors, timeout=3, scroll=False)
        
        # Wait and switch back to original window
        time.sleep(5)
        driver.switch_to.window(original_window)
        print(f"[Profile {profile_idx}] Switched back to main window")
        
        # Wait 15 seconds for login to complete
        print(f"[Profile {profile_idx}] Waiting 15 seconds for login to complete...")
        time.sleep(15)
        
        print(f"[Profile {profile_idx}] Login completed")
        return True
        
    except Exception as e:
        print(f"[Profile {profile_idx}] Login error: {str(e)}")
        return False

def wait_for_logout_button(driver, profile_idx):
    """Wait for logout button to appear (means page loaded)"""
    try:
        logout_selectors = [
            "/html/body/nav/div/div/button/span",
            "//nav//button//span[contains(., 'Logout') or contains(., 'Log out')]",
            "//button[contains(., 'Logout')]",
            "//*[contains(text(), 'Logout')]"
        ]
        
        print(f"[Profile {profile_idx}] Waiting for logout button to appear...")
        
        for selector in logout_selectors:
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print(f"[Profile {profile_idx}] ✅ Logout button found - Page fully loaded")
                return True
            except:
                continue
        
        print(f"[Profile {profile_idx}] ⚠️ Logout button not found, continuing anyway")
        return True
    except Exception as e:
        print(f"[Profile {profile_idx}] Wait error: {str(e)}")
        return True

def visit_x_buttons(driver, profile_idx):
    """Click Visit X buttons and handle new tabs"""
    try:
        # Store original window
        original_window = driver.current_window_handle
        
        # Visit X button 1
        visit_x1_selectors = [
            "/html/body/main/div/div[2]/section/div[6]/div[2]/a/button/b",
            "//button[contains(., 'Visit')]",
            "//a[contains(@href, 'x.com')]//button"
        ]
        
        print(f"[Profile {profile_idx}] Looking for Visit X button 1...")
        if find_and_click(driver, visit_x1_selectors, timeout=10):
            print(f"[Profile {profile_idx}] Clicked Visit X button 1")
            time.sleep(5)
            
            # Switch to new tab and close it
            all_windows = driver.window_handles
            if len(all_windows) > 1:
                driver.switch_to.window(all_windows[-1])
                print(f"[Profile {profile_idx}] Switched to new tab")
                time.sleep(5)
                driver.close()
                print(f"[Profile {profile_idx}] Closed new tab")
                driver.switch_to.window(original_window)
                print(f"[Profile {profile_idx}] Switched back to main tab")
                time.sleep(5)
        else:
            print(f"[Profile {profile_idx}] Visit X button 1 not found")
        
        # Visit X button 2
        visit_x2_selectors = [
            "/html/body/main/div/div[2]/section/div[7]/div[2]/a/button/b",
            "(//button[contains(., 'Visit')])[2]"
        ]
        
        print(f"[Profile {profile_idx}] Looking for Visit X button 2...")
        if find_and_click(driver, visit_x2_selectors, timeout=10):
            print(f"[Profile {profile_idx}] Clicked Visit X button 2")
            time.sleep(5)
            
            # Switch to new tab and close it
            all_windows = driver.window_handles
            if len(all_windows) > 1:
                driver.switch_to.window(all_windows[-1])
                print(f"[Profile {profile_idx}] Switched to new tab")
                time.sleep(5)
                driver.close()
                print(f"[Profile {profile_idx}] Closed new tab")
                driver.switch_to.window(original_window)
                print(f"[Profile {profile_idx}] Switched back to main tab")
                time.sleep(5)
        else:
            print(f"[Profile {profile_idx}] Visit X button 2 not found")
        
        return True
        
    except Exception as e:
        print(f"[Profile {profile_idx}] Visit X error: {str(e)}")
        return False

def claim_rewards(driver, profile_idx):
    """Claim all rewards"""
    try:
        # Scroll and find first Claim Reward button
        first_claim_selectors = [
            "/html/body/main/div/div[2]/div[5]/div/div[2]/button[1]/span",
            "//button[contains(., 'Claim')]//span",
            "//span[contains(., 'Claim reward')]"
        ]
        
        print(f"[Profile {profile_idx}] Looking for first Claim Reward button...")
        if find_and_click(driver, first_claim_selectors, timeout=10):
            print(f"[Profile {profile_idx}] Clicked first Claim Reward")
            print(f"[Profile {profile_idx}] Waiting 2 minutes...")
            time.sleep(120)  # Wait 2 minutes
            
            # Click Okay button
            okay_selectors = [
                "/html/body/div[12]/div[3]/button",
                "//button[contains(., 'Okay')]",
                "//button[contains(., 'OK')]"
            ]
            
            print(f"[Profile {profile_idx}] Looking for Okay button...")
            if find_and_click(driver, okay_selectors, timeout=10):
                print(f"[Profile {profile_idx}] Clicked Okay button")
                time.sleep(2)
        else:
            print(f"[Profile {profile_idx}] First Claim Reward not found")
        
        # Scroll up and claim reward from Visit X 1
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        claim_x1_selectors = [
            "/html/body/main/div/div[2]/section/div[6]/div[2]/button/b",
            "(//button[contains(., 'Claim')])[1]"
        ]
        
        print(f"[Profile {profile_idx}] Looking for Claim Reward (Visit X 1)...")
        if find_and_click(driver, claim_x1_selectors, timeout=10):
            print(f"[Profile {profile_idx}] Claimed reward from Visit X 1")
            time.sleep(2)
        else:
            print(f"[Profile {profile_idx}] Claim Reward (Visit X 1) not found")
        
        # Claim reward from Visit X 2
        claim_x2_selectors = [
            "/html/body/main/div/div[2]/section/div[7]/div[2]/button/b",
            "(//button[contains(., 'Claim')])[2]"
        ]
        
        print(f"[Profile {profile_idx}] Looking for Claim Reward (Visit X 2)...")
        if find_and_click(driver, claim_x2_selectors, timeout=10):
            print(f"[Profile {profile_idx}] Claimed reward from Visit X 2")
            time.sleep(2)
        else:
            print(f"[Profile {profile_idx}] Claim Reward (Visit X 2) not found")
        
        return True
        
    except Exception as e:
        print(f"[Profile {profile_idx}] Claim rewards error: {str(e)}")
        return False

def access_website_with_profile(profile_path, profile_idx):
    """Main function to access website with profile"""
    driver = None
    try:
        print(f"[Profile {profile_idx}] Starting...")
        
        options = Options()
        options.profile = profile_path
        
        # Maximum anti-detection settings
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference('useAutomationExtension', False)
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0")
        options.set_preference("general.platform.override", "Win32")
        options.set_preference("general.appversion.override", "5.0 (Windows)")
        options.set_preference("marionette", False)
        options.set_preference("devtools.console.stdout.content", False)
        options.set_preference("privacy.trackingprotection.enabled", True)
        options.set_preference("geo.enabled", False)
        options.set_preference("media.navigator.enabled", False)
        
        # Hide automation infobar
        options.set_preference("dom.disable_open_during_load", False)
        options.set_preference("browser.startup.page", 0)
        options.set_preference("browser.shell.checkDefaultBrowser", False)
        
        # Set arguments to hide automation
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Add random delay before starting
        random_delay(2, 4)
        
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        
        # Wait a bit before navigating
        random_delay(1, 2)
        
        # Comprehensive stealth script
        stealth_script = """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'permissions', {
                get: () => ({
                    query: () => Promise.resolve({state: 'prompt'})
                })
            });
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8
            });
            Object.defineProperty(navigator, 'deviceMemory', {
                get: () => 8
            });
        """
        driver.execute_script(stealth_script)
        
        # Try loading a simple page first to get cookies
        print(f"[Profile {profile_idx}] Pre-loading to establish session...")
        try:
            driver.get("about:blank")
            random_delay(2, 3)
        except:
            pass
        
        print(f"[Profile {profile_idx}] Loading main page...")
        driver.get(TARGET_URL)
        
        # Wait 15-20 seconds for Cloudflare (reduced)
        wait_time = random.randint(15, 20)
        print(f"[Profile {profile_idx}] Waiting {wait_time} seconds for Cloudflare check...")
        time.sleep(wait_time)
        
        # Multiple human-like scrolls
        human_like_scroll(driver)
        random_delay(2, 4)
        human_like_scroll(driver)
        random_delay(1, 3)
        
        print(f"[Profile {profile_idx}] Page loaded")
        
        # Step 1: Login with Google
        login_with_google(driver, profile_idx)
        
        # Step 2: Wait for page to load completely (check logout button)
        wait_for_logout_button(driver, profile_idx)
        time.sleep(3)
        
        # Step 3: Visit X buttons
        visit_x_buttons(driver, profile_idx)
        time.sleep(5)
        
        # Step 4: Claim rewards
        claim_rewards(driver, profile_idx)
        
        # Wait before closing
        print(f"[Profile {profile_idx}] All tasks completed. Waiting before closing...")
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

def run_batch(profiles, batch_num, max_workers=2):
    """Run batch of profiles - REDUCED to 2 workers to avoid Cloudflare"""
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
    print("Firefox Multi-Profile Automation - Kindred Labs")
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
        all_results.extend(run_batch(batch, i, max_workers=2))  # Only 2 at a time
        if i < len(batches):
            wait_time = random.randint(15, 25)
            print(f"\nWaiting {wait_time} seconds before next batch...\n")
            time.sleep(wait_time)
    
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
