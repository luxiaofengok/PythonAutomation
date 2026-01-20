from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import threading
import os
import shutil
import tempfile
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed

# URL to access
TARGET_URL = "https://app.tria.so/rewards"

# Define the path to your Firefox profiles
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

def clean_temp_files():
    """
    Clean temporary files to free up disk space
    """
    try:
        print("[Cleanup] Starting cleanup of temporary files...")
        
        # Clean Windows temp folder
        temp_dir = tempfile.gettempdir()
        
        # Clean Firefox temp files
        firefox_temp_patterns = [
            os.path.join(temp_dir, "tmp*.tmp"),
            os.path.join(temp_dir, "*.tmp"),
            os.path.join(temp_dir, "rust_mozprofile*"),
            os.path.join(temp_dir, "firefox_*"),
            os.path.join(temp_dir, "tmpaddon*"),
            os.path.join(temp_dir, "webdriver-py-*"),
            os.path.join(temp_dir, "tmp*"),
        ]
        
        removed_count = 0
        failed_count = 0
        
        for pattern in firefox_temp_patterns:
            for file_path in glob.glob(pattern):
                try:
                    if os.path.isfile(file_path):
                        # Check if file is older than 1 minute to avoid deleting files in use
                        if time.time() - os.path.getmtime(file_path) > 60:
                            os.remove(file_path)
                            removed_count += 1
                    elif os.path.isdir(file_path):
                        # Check if directory is older than 1 minute
                        if time.time() - os.path.getmtime(file_path) > 60:
                            shutil.rmtree(file_path, ignore_errors=True)
                            removed_count += 1
                except Exception as e:
                    failed_count += 1
                    pass  # Skip files that are in use
        
        print(f"[Cleanup] Removed {removed_count} temporary items, {failed_count} items in use (skipped)")
        
        # Try to clean using system command for more aggressive cleanup
        try:
            import subprocess
            # Delete old temp files using PowerShell (files older than 1 day)
            ps_command = f'Get-ChildItem -Path "{temp_dir}" -Filter "tmp*" -File | Where-Object {{$_.LastWriteTime -lt (Get-Date).AddDays(-1)}} | Remove-Item -Force -ErrorAction SilentlyContinue'
            subprocess.run(["powershell", "-Command", ps_command], capture_output=True, timeout=10)
            print("[Cleanup] PowerShell cleanup executed")
        except:
            pass
        
    except Exception as e:
        print(f"[Cleanup] Error during cleanup: {str(e)}")

def clean_profile_cache(profile_path):
    """
    Clean cache and temporary files from Firefox profile
    """
    try:
        cache_folders = [
            "cache2",
            "thumbnails",
            "OfflineCache",
            "startupCache",
            "shader-cache",
        ]
        
        for folder in cache_folders:
            cache_path = os.path.join(profile_path, folder)
            if os.path.exists(cache_path):
                try:
                    shutil.rmtree(cache_path, ignore_errors=True)
                except:
                    pass
        
    except Exception as e:
        pass  # Silently fail if cache cleaning doesn't work

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
        
        # Optimize Firefox to reduce disk usage
        options.set_preference("browser.cache.disk.enable", False)
        options.set_preference("browser.cache.memory.enable", True)
        options.set_preference("browser.cache.offline.enable", False)
        options.set_preference("browser.sessionstore.resume_from_crash", False)
        options.set_preference("browser.cache.disk.capacity", 0)
        options.set_preference("browser.cache.disk.smart_size.enabled", False)
        
        # Initialize Firefox driver
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 30)
        
        # Access the target URL
        driver.get(TARGET_URL)
        print(f"[Profile {profile_index}] Successfully accessed: {TARGET_URL}")
        
        # Wait for page to fully load
        time.sleep(5)
        
        # Step 1: Login with Google (no login button needed, form appears directly)
        try:
            print(f"[Profile {profile_index}] Waiting for page to load completely...")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Check if already logged in by looking for rewards page elements
            print(f"[Profile {profile_index}] Checking if already logged in...")
            try:
                # Try to find elements that appear when logged in
                logged_in_check = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(., 'TRIA Rewards') or contains(., 'Boosted Rewards') or contains(., 'Today')]"))
                )
                print(f"[Profile {profile_index}] Already logged in, skipping login step")
                raise TimeoutException("Already logged in")
            except:
                print(f"[Profile {profile_index}] Not logged in, proceeding with Google login...")
            
            # Click "Continue with Google" button directly
            print(f"[Profile {profile_index}] Looking for 'Continue with Google' button...")
            google_button = None
            google_selectors = [
                "//button[contains(., 'Continue with Google')]",
                "//button[contains(., 'Google')]",
                "//button[contains(., 'Sign in with Google')]",
                "//*[contains(@class, 'google')]//button",
                "//button[contains(@aria-label, 'Google')]",
                "//*[name()='svg' and contains(@class, 'google')]/ancestor::button",
                "//button[.//text()[contains(., 'Google')]]"
            ]
            
            for selector in google_selectors:
                try:
                    google_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"[Profile {profile_index}] Google button found with selector: {selector}")
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
                print(f"[Profile {profile_index}] Could not find 'Continue with Google' button - may already be logged in")
                raise TimeoutException("No Google button")
            
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
        
        # Step 2: Wait for page to load completely after login
        print(f"[Profile {profile_index}] Waiting for system to fully load...")
        time.sleep(8)  # Wait for the system to load completely
        
        # Step 3: Click on a random position on the right side of screen to dismiss any popups
        try:
            print(f"[Profile {profile_index}] Clicking right side of screen to dismiss popups...")
            # Get window size
            window_width = driver.execute_script("return window.innerWidth;")
            window_height = driver.execute_script("return window.innerHeight;")
            
            # Click on the right side (80% of width, 50% of height)
            right_x = int(window_width * 0.8)
            middle_y = int(window_height * 0.5)
            
            # Use ActionChains to click at coordinates
            actions = ActionChains(driver)
            actions.move_by_offset(right_x, middle_y).click().perform()
            time.sleep(2)
            
            # Reset the mouse position
            actions = ActionChains(driver)
            actions.move_by_offset(-right_x, -middle_y).perform()
            
            print(f"[Profile {profile_index}] Clicked right side of screen")
        except Exception as e:
            print(f"[Profile {profile_index}] Error clicking right side: {str(e)}")
        
        # Step 4: Find and click Rewards button
        try:
            print(f"[Profile {profile_index}] Looking for Rewards button...")
            
            # Try multiple selectors for Rewards button
            rewards_selectors = [
                "//button[contains(translate(., 'REWARDS', 'rewards'), 'rewards')]",
                "//button[contains(., 'Rewards')]",
                "//a[contains(., 'Rewards')]",
                "//*[contains(text(), 'Rewards') or contains(text(), 'REWARDS')]",
                "//div[contains(@class, 'rewards')]//button",
                "//nav//button[contains(., 'Rewards')]",
                "//nav//a[contains(., 'Rewards')]"
            ]
            
            rewards_button = None
            for selector in rewards_selectors:
                try:
                    rewards_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"[Profile {profile_index}] Rewards button found with selector: {selector}")
                    break
                except:
                    continue
            
            if rewards_button:
                print(f"[Profile {profile_index}] Clicking Rewards button...")
                driver.execute_script("arguments[0].scrollIntoView(true);", rewards_button)
                time.sleep(1)
                try:
                    rewards_button.click()
                except:
                    driver.execute_script("arguments[0].click();", rewards_button)
                
                time.sleep(3)
                print(f"[Profile {profile_index}] Rewards button clicked successfully")
            else:
                print(f"[Profile {profile_index}] Could not find Rewards button - may already be on Rewards page")
        except Exception as e:
            print(f"[Profile {profile_index}] Error with Rewards button: {str(e)}")
        
        # Step 5: Find checkin button and scroll it to center of screen
        try:
            print(f"[Profile {profile_index}] Looking for checkin button...")
            
            # Try multiple selectors for checkin button
            checkin_selectors = [
                "//button[contains(translate(., 'CHECKIN', 'checkin'), 'checkin')]",
                "//button[contains(., 'Check in')]",
                "//button[contains(., 'Check-in')]",
                "//button[contains(., 'Checkin')]",
                "//button[contains(., 'check in')]",
                "//*[contains(text(), 'Check in') or contains(text(), 'Checkin') or contains(text(), 'CHECK IN')]"
            ]
            
            checkin_button = None
            for selector in checkin_selectors:
                try:
                    checkin_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    print(f"[Profile {profile_index}] Checkin button found with selector: {selector}")
                    break
                except:
                    continue
            
            if checkin_button:
                # Scroll the button to center of screen
                print(f"[Profile {profile_index}] Scrolling checkin button to center of screen...")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", checkin_button)
                time.sleep(5)
                
                # Click the checkin button
                print(f"[Profile {profile_index}] Clicking checkin button...")
                try:
                    # Try normal click first
                    checkin_button.click()
                except:
                    # If normal click fails, use JavaScript click
                    driver.execute_script("arguments[0].click();", checkin_button)
                
                print(f"[Profile {profile_index}] Checkin button clicked successfully")
                
                # Wait for modal to fully appear
                print(f"[Profile {profile_index}] Waiting for modal to appear...")
                time.sleep(1)
                
                # Click the final checkin button in the modal/popup
                print(f"[Profile {profile_index}] Looking for final checkin confirmation button...")
                try:
                    # Try multiple selectors for the final button
                    final_button_selectors = [
                        "//button[text()='Check in']",
                        "//button[contains(text(), 'Check in')]",
                        "//div[contains(@class, 'modal')]//button[text()='Check in']",
                        "/html/body/div[13]/div/div[3]/button",
                        "//div[@role='dialog']//button[contains(., 'Check in')]",
                        "//button[contains(@class, 'check')]",
                        "(//button[contains(., 'Check in')])[last()]"
                    ]
                    
                    final_checkin_button = None
                    for selector in final_button_selectors:
                        try:
                            final_checkin_button = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, selector))
                            )
                            # Make sure it's visible and clickable
                            if final_checkin_button.is_displayed():
                                print(f"[Profile {profile_index}] Final checkin button found with selector: {selector}")
                                break
                            else:
                                final_checkin_button = None
                        except:
                            continue
                    
                    if final_checkin_button:
                        # Scroll button into view
                        print(f"[Profile {profile_index}] Scrolling final button into view...")
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", final_checkin_button)
                        time.sleep(2)
                        
                        print(f"[Profile {profile_index}] Clicking final checkin button...")
                        
                        # Try multiple methods to click
                        clicked = False
                        
                        # Method 1: JavaScript click (most reliable for modals)
                        try:
                            driver.execute_script("arguments[0].click();", final_checkin_button)
                            clicked = True
                            print(f"[Profile {profile_index}] Clicked using JavaScript")
                        except Exception as e:
                            print(f"[Profile {profile_index}] JavaScript click failed: {str(e)}")
                        
                        # Method 2: ActionChains click
                        if not clicked:
                            try:
                                actions = ActionChains(driver)
                                actions.move_to_element(final_checkin_button).pause(1).click().perform()
                                clicked = True
                                print(f"[Profile {profile_index}] Clicked using ActionChains")
                            except Exception as e:
                                print(f"[Profile {profile_index}] ActionChains click failed: {str(e)}")
                        
                        # Method 3: Regular click
                        if not clicked:
                            try:
                                final_checkin_button.click()
                                clicked = True
                                print(f"[Profile {profile_index}] Clicked using regular click")
                            except Exception as e:
                                print(f"[Profile {profile_index}] Regular click failed: {str(e)}")
                        
                        # Wait 5 seconds after clicking
                        time.sleep(5)
                        
                        if clicked:
                            print(f"[Profile {profile_index}] Successfully checked in!")
                        else:
                            print(f"[Profile {profile_index}] Could not click final button - all methods failed")
                    else:
                        print(f"[Profile {profile_index}] Could not find final checkin button with any selector")
                    
                except TimeoutException:
                    print(f"[Profile {profile_index}] Timeout waiting for final checkin confirmation button")
                except Exception as e:
                    print(f"[Profile {profile_index}] Error clicking final checkin button: {str(e)}")
                    
            else:
                print(f"[Profile {profile_index}] Could not find checkin button")
            
        except TimeoutException:
            print(f"[Profile {profile_index}] Timeout while looking for checkin button")
        except Exception as e:
            print(f"[Profile {profile_index}] Error in checkin step: {str(e)}")
        
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
    clean_temp_files()
    
    return results

def main():
    """
    Main function to run all batches
    """
    print("="*60)
    print("Firefox Multi-Profile Automation Script - Tria Checkin")
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
    
    # Wait between batches
    print("\nWaiting 8 seconds before starting next batch...\n")
    time.sleep(8)
    
    # Run Batch 2
    batch2_results = run_batch(batch2, 2, max_workers=8)
    all_results.extend(batch2_results)
    
    # Wait between batches
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
    
    # Additional aggressive cleanup for temp files
    try:
        print("[Final Cleanup] Running aggressive cleanup...")
        temp_dir = tempfile.gettempdir()
        
        # Count all tmp files
        all_tmp_files = glob.glob(os.path.join(temp_dir, "tmp*"))
        print(f"[Final Cleanup] Found {len(all_tmp_files)} tmp files/folders")
        
        # Try to remove them one by one
        removed = 0
        for tmp_file in all_tmp_files:
            try:
                if os.path.isfile(tmp_file):
                    os.remove(tmp_file)
                    removed += 1
                elif os.path.isdir(tmp_file):
                    shutil.rmtree(tmp_file, ignore_errors=True)
                    removed += 1
            except:
                pass
        
        print(f"[Final Cleanup] Removed {removed} additional temp items")
        
        # Show remaining temp files
        remaining = len(glob.glob(os.path.join(temp_dir, "tmp*")))
        print(f"[Final Cleanup] {remaining} temp items remaining (likely in use)")
        
    except Exception as e:
        print(f"[Final Cleanup] Error in aggressive cleanup: {str(e)}")
    
    print("[Final Cleanup] Cleanup completed!")

if __name__ == "__main__":
    main()
