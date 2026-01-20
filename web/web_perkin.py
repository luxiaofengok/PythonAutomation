from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import cleanup functions from framework
from web_source import clean_temp_files, clean_profile_cache

# URL to access
TARGET_URL = "https://perkinsrwa.com/task"

# Define the path to your Firefox profiles
# Using actual profile folder names with "Hồ sơ"
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

def access_website_with_profile(profile_path, profile_index):
    """
    Access the target website using a specific Firefox profile
    """
    driver = None
    try:
        print(f"[Profile {profile_index}] Starting browser with profile: {profile_path}")
        
        # Configure Firefox options
        options = Options()
        options.profile = profile_path
        
        # Optional: Run in headless mode (remove these lines if you want to see the browser)
        # options.add_argument('--headless')
        
        # Initialize Firefox driver
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 30)  # Increased timeout
        
        # Access the target URL
        driver.get(TARGET_URL)
        print(f"[Profile {profile_index}] Successfully accessed: {TARGET_URL}")
        
        # Wait for page to fully load
        time.sleep(5)
        
        # Step 1: Check for login button
        try:
            print(f"[Profile {profile_index}] Waiting for page to load completely...")
            # Wait for body to be present
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            print(f"[Profile {profile_index}] Checking for login button...")
            # Try multiple possible selectors for login button
            login_button = None
            selectors = [
                "//button[contains(translate(., 'LOGIN', 'login'), 'login')]",
                "//button[contains(., 'Login')]",
                "//a[contains(translate(., 'LOGIN', 'login'), 'login')]",
                "//div[contains(@class, 'login')]//button",
                "//*[contains(text(), 'Login') or contains(text(), 'LOG IN') or contains(text(), 'log in')]"
            ]
            
            for selector in selectors:
                try:
                    login_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"[Profile {profile_index}] Login button found with selector: {selector}")
                    break
                except:
                    continue
            
            if login_button:
                print(f"[Profile {profile_index}] Clicking login button...")
                driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
                time.sleep(1)
                login_button.click()
                time.sleep(3)
                
                # Click "Continue with Google" button
                print(f"[Profile {profile_index}] Looking for 'Continue with Google' button...")
                google_button = None
                google_selectors = [
                    "//button[contains(., 'Continue with Google')]",
                    "//button[contains(., 'Google')]",
                    "//*[contains(@class, 'google')]//button",
                    "//button[contains(@aria-label, 'Google')]",
                    "//*[name()='svg' and contains(@class, 'google')]/ancestor::button"
                ]
                
                for selector in google_selectors:
                    try:
                        google_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        print(f"[Profile {profile_index}] Google button found!")
                        break
                    except:
                        continue
                
                if google_button:
                    print(f"[Profile {profile_index}] Clicking 'Continue with Google'...")
                    driver.execute_script("arguments[0].scrollIntoView(true);", google_button)
                    time.sleep(1)
                    google_button.click()
                    time.sleep(5)
                else:
                    print(f"[Profile {profile_index}] Could not find 'Continue with Google' button")
            else:
                print(f"[Profile {profile_index}] No login button found - checking if already logged in...")
                raise TimeoutException("No login button")
            
            # Click the specific Google account option
            print(f"[Profile {profile_index}] Selecting Google account...")
            try:
                # Wait for Google login page to load
                time.sleep(3)
                
                # Try multiple selectors for Google account
                account_selectors = [
                    "/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div[1]/span/section/div/div/div/div/ul/li[1]/div",
                    "//li[1]//div[@role='link']",
                    "//div[@data-authuser='0']",
                    "//ul//li[1]//div[contains(@class, 'BHzsHc')]",
                    "(//div[contains(@jsname, 'V67aGc')])[1]"
                ]
                
                google_account = None
                for selector in account_selectors:
                    try:
                        google_account = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        print(f"[Profile {profile_index}] Google account found!")
                        break
                    except:
                        continue
                
                if google_account:
                    google_account.click()
                    time.sleep(3)
                else:
                    print(f"[Profile {profile_index}] No account selection needed or already logged in")
            except Exception as e:
                print(f"[Profile {profile_index}] Account selection: {str(e)}")
            
            # Click continue button if present
            print(f"[Profile {profile_index}] Looking for continue button...")
            try:
                continue_selectors = [
                    "//button[contains(., 'Continue')]",
                    "//button[contains(., 'Tiếp tục')]",
                    "//button[@type='button' and contains(@class, 'VfPpkd-LgbsSe')]"
                ]
                
                for selector in continue_selectors:
                    try:
                        continue_button = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        continue_button.click()
                        print(f"[Profile {profile_index}] Continue button clicked")
                        time.sleep(3)
                        break
                    except:
                        continue
            except:
                print(f"[Profile {profile_index}] No continue button found, proceeding...")
            
            print(f"[Profile {profile_index}] Login process completed")
            
        except TimeoutException:
            print(f"[Profile {profile_index}] No login button found - already logged in")
        except Exception as e:
            print(f"[Profile {profile_index}] Login error (continuing anyway): {str(e)}")
        
        # Wait for page to stabilize after login
        print(f"[Profile {profile_index}] Waiting for page to stabilize...")
        time.sleep(5)
        
        # Step 2: Click on Earn
        try:
            print(f"[Profile {profile_index}] Looking for 'Earn' button...")
            
            # Try multiple selectors for Earn button
            earn_selectors = [
                "//button[contains(translate(., 'EARN', 'earn'), 'earn')]",
                "//a[contains(translate(., 'EARN', 'earn'), 'earn')]",
                "//div[contains(@class, 'earn')]",
                "//*[contains(text(), 'Earn') or contains(text(), 'EARN')]"
            ]
            
            earn_button = None
            for selector in earn_selectors:
                try:
                    earn_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"[Profile {profile_index}] Earn button found!")
                    break
                except:
                    continue
            
            if earn_button:
                print(f"[Profile {profile_index}] Clicking 'Earn' button...")
                driver.execute_script("arguments[0].scrollIntoView(true);", earn_button)
                time.sleep(1)
                earn_button.click()
                time.sleep(4)
                
                # Click on the specific image/element
                print(f"[Profile {profile_index}] Looking for task element...")
                task_selectors = [
                    "/html/body/div[1]/div/div[3]/div/div[2]/div[3]/div[1]/div[2]/div/img",
                    "//img[contains(@class, 'task')]",
                    "//div[contains(@class, 'task')]//img",
                    "(//img)[1]"
                ]
                
                task_element = None
                for selector in task_selectors:
                    try:
                        task_element = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        print(f"[Profile {profile_index}] Task element found!")
                        break
                    except:
                        continue
                
                if task_element:
                    driver.execute_script("arguments[0].scrollIntoView(true);", task_element)
                    time.sleep(1)
                    task_element.click()
                    time.sleep(2)
                    print(f"[Profile {profile_index}] Successfully clicked on earn task")
                else:
                    print(f"[Profile {profile_index}] Could not find task element")
            else:
                print(f"[Profile {profile_index}] Could not find earn button")
            
        except TimeoutException:
            print(f"[Profile {profile_index}] Could not find earn button or task element")
        except Exception as e:
            print(f"[Profile {profile_index}] Error in earn step: {str(e)}")
        
        # Keep browser open for a while to see results
        print(f"[Profile {profile_index}] Waiting before closing browser...")
        time.sleep(10)
        
        print(f"[Profile {profile_index}] Task completed")
        
        return f"Profile {profile_index}: Success"
        
    except Exception as e:
        print(f"[Profile {profile_index}] Error: {str(e)}")
        return f"Profile {profile_index}: Failed - {str(e)}"
        
    finally:
        if driver:
            driver.quit()
            print(f"[Profile {profile_index}] Browser closed")
        
        # Clean up cache and temp files after closing browser
        try:
            print(f"[Profile {profile_index}] Cleaning profile cache...")
            clean_profile_cache(profile_path)
        except:
            pass

def run_batch(batch_profiles, batch_number, max_workers=8):
    """
    Run a batch of profiles concurrently
    """
    print(f"\n{'='*60}")
    print(f"Starting Batch {batch_number} with {len(batch_profiles)} profiles")
    print(f"{'='*60}\n")
    
    results = []
    
    # Use ThreadPoolExecutor to run multiple profiles concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_profile = {
            executor.submit(access_website_with_profile, profile[0], profile[1]): profile 
            for profile in batch_profiles
        }
        
        # Wait for all tasks to complete
        for future in as_completed(future_to_profile):
            profile = future_to_profile[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Profile {profile[1]} generated an exception: {e}")
                results.append(f"Profile {profile[1]}: Exception - {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"Batch {batch_number} completed")
    print(f"{'='*60}\n")
    
    # Clean temp files after each batch
    print(f"[Batch {batch_number}] Cleaning temp files...")
    clean_temp_files()
    
    return results

def main():
    """
    Main function to run all batches
    """
    print("="*60)
    print("Firefox Multi-Profile Automation Script")
    print("="*60)
    print(f"Target URL: {TARGET_URL}")
    print(f"Total Profiles: {len(FIREFOX_PROFILES)}")
    print(f"Batches: 3 (8 + 8 + 6)")
    print("="*60)
    
    # Prepare batches
    # Batch 1: First 8 profiles
    batch1 = [(FIREFOX_PROFILES[i], i+1) for i in range(8)]
    
    # Batch 2: Next 8 profiles
    batch2 = [(FIREFOX_PROFILES[i], i+1) for i in range(8, 16)]
    
    # Batch 3: Last 6 profiles
    batch3 = [(FIREFOX_PROFILES[i], i+1) for i in range(16, 22)]
    
    all_results = []
    
    # Run Batch 1
    batch1_results = run_batch(batch1, 1, max_workers=8)
    all_results.extend(batch1_results)
    
    # Wait between batches (adjust as needed)
    print("\nWaiting 8 seconds before starting next batch...\n")
    time.sleep(8)
    
    # Run Batch 2
    batch2_results = run_batch(batch2, 2, max_workers=8)
    all_results.extend(batch2_results)
    
    # Wait between batches (adjust as needed)
    print("\nWaiting 8 seconds before starting next batch...\n")
    time.sleep(8)
    
    # Run Batch 3
    batch3_results = run_batch(batch3, 3, max_workers=6)
    all_results.extend(batch3_results)
    
    # Print summary
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    for result in all_results:
        print(result)
    print("="*60)
    print("All batches completed!")
    print("="*60)
    
    # Final cleanup
    print("\n[Final Cleanup] Performing final cleanup...")
    clean_temp_files()
    print("[Final Cleanup] Cleanup completed!")

if __name__ == "__main__":
    main()
