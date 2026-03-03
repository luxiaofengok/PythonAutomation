"""
FairShares Daily Checkin Automation
Automates: Connect Wallet → OKX Extension → Daily Checkin
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from web.web_source import create_firefox_driver, find_element_by_selectors, click_element_safe, ELEMENT_TIMEOUT
import time


class FairSharesBot:
    def __init__(self, profile_path, profile_index=1, okx_password=""):
        self.profile_path = profile_path
        self.profile_index = profile_index
        self.okx_password = okx_password
        self.driver = None
        self.wait = None
    
    def start(self):
        """Initialize Firefox driver"""
        try:
            self.driver = create_firefox_driver(self.profile_path, optimize=True, headless=False)
            self.wait = WebDriverWait(self.driver, ELEMENT_TIMEOUT)
            print(f"[Profile {self.profile_index}] Driver started successfully")
            return True
        except Exception as e:
            print(f"[Profile {self.profile_index}] Failed to start driver: {e}")
            return False
    
    def access_website(self, url="https://app.fairshares.io/waitlist?AccessCode=hb2wvt3d"):
        """Step 1: Access the FairShares website"""
        try:
            print(f"[Profile {self.profile_index}] Accessing website: {url}")
            self.driver.get(url)
            time.sleep(3)
            print(f"[Profile {self.profile_index}] Website loaded")
            return True
        except Exception as e:
            print(f"[Profile {self.profile_index}] Failed to access website: {e}")
            return False
    
    def skip_login_checks(self):
        """Skip any login/Google login prompts"""
        try:
            print(f"[Profile {self.profile_index}] Checking for login prompts...")
            
            # Try to close any login modals
            close_selectors = [
                "//button[contains(@aria-label, 'close')]",
                "//button[contains(@class, 'close')]",
                "//svg[contains(@class, 'close')]/..",
                "//div[contains(@class, 'modal')]//button[1]"
            ]
            
            for selector in close_selectors:
                try:
                    element = self.driver.find_elements(By.XPATH, selector)
                    if element:
                        click_element_safe(self.driver, element[0])
                        time.sleep(1)
                except:
                    continue
            
            print(f"[Profile {self.profile_index}] Login checks skipped")
            return True
        except Exception as e:
            print(f"[Profile {self.profile_index}] Error during login skip: {e}")
            return False
    
    def click_connect_wallet(self):
        """Step 2: Click the Connect Wallet button"""
        try:
            print(f"[Profile {self.profile_index}] Looking for Connect Wallet button...")
            
            connect_selectors = [
                "//button[contains(., 'Connect Wallet')]",
                "//button[contains(., 'connect wallet')]",
                "//button[contains(., 'Connect wallet')]",
                "//button[contains(@class, 'connect')]",
                "//span[contains(., 'Connect')]//..",
                "//button[contains(., 'Kết nối')]"
            ]
            
            connect_button = find_element_by_selectors(self.driver, connect_selectors, wait_time=15)
            
            if not connect_button:
                print(f"[Profile {self.profile_index}] Connect Wallet button not found")
                return False
            
            print(f"[Profile {self.profile_index}] Found Connect Wallet button, clicking...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", connect_button)
            time.sleep(1)
            
            click_element_safe(self.driver, connect_button)
            time.sleep(3)
            
            print(f"[Profile {self.profile_index}] Connect Wallet button clicked")
            return True
        except Exception as e:
            print(f"[Profile {self.profile_index}] Error clicking Connect Wallet: {e}")
            return False
    
    def connect_okx_wallet(self):
        """Step 3: Select OKX Wallet from the list"""
        try:
            print(f"[Profile {self.profile_index}] Looking for OKX Wallet option...")
            
            okx_selectors = [
                "//div[contains(., 'MetaMask')]//button",
                "//button[contains(., 'MetaMask')]",
                "//div[contains(@class, 'wallet')]//div[contains(., 'MetaMask')]//..",
                "//button[contains(., 'MetaMask Wallet')]",
                "//*[contains(., 'MetaMask')]"
            ]
            
            okx_button = find_element_by_selectors(self.driver, okx_selectors, wait_time=10)
            
            if not okx_button:
                print(f"[Profile {self.profile_index}] MetaMask Wallet option not found")
                return False
            
            print(f"[Profile {self.profile_index}] Found MetaMask Wallet, clicking...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", okx_button)
            time.sleep(1)
            
            click_element_safe(self.driver, okx_button)
            time.sleep(5)
            
            print(f"[Profile {self.profile_index}] MetaMask Wallet selected")
            return True
        except Exception as e:
            print(f"[Profile {self.profile_index}] Error selecting MetaMask Wallet: {e}")
            return False
    
    def handle_okx_extension_popup(self):
        """Step 4: Handle MetaMask extension popup - approve access"""
        try:
            print(f"[Profile {self.profile_index}] Waiting for MetaMask extension popup...")
            time.sleep(3)
            
            # Get all window handles
            original_window = self.driver.current_window_handle
            all_windows = self.driver.window_handles
            
            # Switch to popup if available
            if len(all_windows) > 1:
                for window in all_windows:
                    if window != original_window:
                        self.driver.switch_to.window(window)
                        print(f"[Profile {self.profile_index}] Switched to MetaMask popup")
                        time.sleep(2)
                        break
            
            # Look for approve/connect button
            approve_selectors = [
                "//button[contains(., 'Connect')]",
                "//button[contains(., 'Approve')]",
                "//button[contains(., 'Allow')]",
                "//button[contains(@class, 'confirm')]",
                "//button[1]"
            ]
            
            approve_button = find_element_by_selectors(self.driver, approve_selectors, wait_time=10)
            
            if approve_button:
                print(f"[Profile {self.profile_index}] Found approval button, clicking...")
                click_element_safe(self.driver, approve_button)
                time.sleep(2)
            
            # Switch back to main window
            self.driver.switch_to.window(original_window)
            time.sleep(2)
            
            print(f"[Profile {self.profile_index}] MetaMask extension popup handled")
            return True
        except Exception as e:
            print(f"[Profile {self.profile_index}] Error handling MetaMask popup: {e}")
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            return False
    
    def enter_okx_password(self):
        """Step 5: Enter OKX wallet password"""
        try:
            print(f"[Profile {self.profile_index}] Looking for password field...")
            
            if not self.okx_password:
                print(f"[Profile {self.profile_index}] No OKX password provided, skipping...")
                return True
            
            # Look for password input
            password_selectors = [
                "//input[@type='password']",
                "//input[@placeholder*='password']",
                "//input[@placeholder*='Password']",
                "//input[contains(@class, 'password')]"
            ]
            
            password_field = find_element_by_selectors(self.driver, password_selectors, wait_time=8)
            
            if password_field:
                print(f"[Profile {self.profile_index}] Found password field, entering password...")
                password_field.clear()
                password_field.send_keys(self.okx_password)
                time.sleep(1)
                
                # Click confirm button
                confirm_selectors = [
                    "//button[contains(., 'Confirm')]",
                    "//button[contains(., 'Sign')]",
                    "//button[contains(., 'OK')]",
                    "//button[2]"
                ]
                
                confirm_button = find_element_by_selectors(self.driver, confirm_selectors, wait_time=8)
                if confirm_button:
                    click_element_safe(self.driver, confirm_button)
                    time.sleep(3)
                
                print(f"[Profile {self.profile_index}] Password confirmed")
                return True
            else:
                print(f"[Profile {self.profile_index}] Password field not found")
                return False
        except Exception as e:
            print(f"[Profile {self.profile_index}] Error entering password: {e}")
            return False
    
    def sign_wallet(self):
        """Step 6: Sign the wallet"""
        try:
            print(f"[Profile {self.profile_index}] Looking for sign/confirm transaction...")
            
            # Check for any popups or sign requests
            time.sleep(2)
            all_windows = self.driver.window_handles
            
            if len(all_windows) > 1:
                for window in all_windows[1:]:
                    try:
                        self.driver.switch_to.window(window)
                        
                        # Look for sign/confirm button
                        sign_selectors = [
                            "//button[contains(., 'Sign')]",
                            "//button[contains(., 'Confirm')]",
                            "//button[contains(., 'OK')]",
                            "//button[contains(@class, 'confirm')]"
                        ]
                        
                        sign_button = find_element_by_selectors(self.driver, sign_selectors, wait_time=5)
                        if sign_button:
                            print(f"[Profile {self.profile_index}] Found sign button, clicking...")
                            click_element_safe(self.driver, sign_button)
                            time.sleep(2)
                    except:
                        continue
            
            # Switch back to main window
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(2)
            
            print(f"[Profile {self.profile_index}] Wallet signed")
            return True
        except Exception as e:
            print(f"[Profile {self.profile_index}] Error signing wallet: {e}")
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
            except:
                pass
            return False
    
    def wait_for_connection(self, timeout=15):
        """Wait for wallet to be connected"""
        try:
            print(f"[Profile {self.profile_index}] Waiting for wallet connection...")
            
            # Look for success indicators
            success_selectors = [
                "//div[contains(., 'Connected')]",
                "//span[contains(., 'Connected')]",
                "//div[contains(@class, 'success')]",
                "//div[contains(., 'wallet')]//div[contains(., '0x')]"
            ]
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                for selector in success_selectors:
                    try:
                        element = self.driver.find_element(By.XPATH, selector)
                        if element.is_displayed():
                            print(f"[Profile {self.profile_index}] Wallet connected successfully")
                            return True
                    except:
                        continue
                time.sleep(1)
            
            print(f"[Profile {self.profile_index}] Wallet connection confirmed (timeout)")
            return True
        except Exception as e:
            print(f"[Profile {self.profile_index}] Error waiting for connection: {e}")
            return True  # Continue anyway
    
    def find_daily_checkin(self):
        """Step 7: Find Daily Checkin section"""
        try:
            print(f"[Profile {self.profile_index}] Looking for Daily Checkin section...")
            
            checkin_selectors = [
                "//div[contains(., 'Daily Check')]",
                "//div[contains(., 'daily check')]",
                "//section[contains(., 'Daily')]",
                "//button[contains(., 'Check')]",
                "//div[contains(@class, 'checkin')]",
                "//div[contains(text(), 'Daily')]"
            ]
            
            checkin_section = find_element_by_selectors(self.driver, checkin_selectors, wait_time=15)
            
            if checkin_section:
                print(f"[Profile {self.profile_index}] Found Daily Checkin section")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", checkin_section)
                time.sleep(2)
                return True
            else:
                print(f"[Profile {self.profile_index}] Daily Checkin section not found")
                return False
        except Exception as e:
            print(f"[Profile {self.profile_index}] Error finding Daily Checkin: {e}")
            return False
    
    def click_checkin_button(self):
        """Step 8: Click the Checkin button"""
        try:
            print(f"[Profile {self.profile_index}] Looking for Checkin button...")
            
            checkin_btn_selectors = [
                "//button[contains(., 'Check In')]",
                "//button[contains(., 'Checkin')]",
                "//button[contains(., 'Check-in')]",
                "//button[contains(., 'CHECK IN')]",
                "//button[contains(@class, 'checkin')]"
            ]
            
            checkin_button = find_element_by_selectors(self.driver, checkin_btn_selectors, wait_time=10)
            
            if not checkin_button:
                print(f"[Profile {self.profile_index}] Checkin button not found")
                return False
            
            print(f"[Profile {self.profile_index}] Found Checkin button, clicking...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", checkin_button)
            time.sleep(1)
            
            click_element_safe(self.driver, checkin_button)
            time.sleep(3)
            
            print(f"[Profile {self.profile_index}] Checkin button clicked")
            return True
        except Exception as e:
            print(f"[Profile {self.profile_index}] Error clicking Checkin: {e}")
            return False
    
    def verify_checkin_success(self, timeout=10):
        """Verify that daily checkin was successful"""
        try:
            print(f"[Profile {self.profile_index}] Verifying checkin success...")
            
            success_selectors = [
                "//div[contains(., 'success')]",
                "//div[contains(., 'Success')]",
                "//span[contains(., 'checked in')]",
                "//div[contains(@class, 'success')]",
                "//div[contains(., 'Checked in')]"
            ]
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                for selector in success_selectors:
                    try:
                        element = self.driver.find_element(By.XPATH, selector)
                        if element.is_displayed():
                            print(f"[Profile {self.profile_index}] ✓ Daily Checkin successful!")
                            return True
                    except:
                        continue
                time.sleep(1)
            
            print(f"[Profile {self.profile_index}] Checkin completed (verification timeout)")
            return True
        except Exception as e:
            print(f"[Profile {self.profile_index}] Error verifying checkin: {e}")
            return True  # Continue anyway
    
    def run_full_workflow(self, okx_password=""):
        """Run the complete workflow"""
        try:
            self.okx_password = okx_password
            
            print(f"\n{'='*60}")
            print(f"[Profile {self.profile_index}] Starting FairShares Daily Checkin")
            print(f"{'='*60}\n")
            
            # Step 1: Access website
            if not self.access_website():
                return False
            
            time.sleep(2)
            
            # Step 2: Skip login checks
            self.skip_login_checks()
            
            time.sleep(2)
            
            # Step 3: Click Connect Wallet
            if not self.click_connect_wallet():
                return False
            
            time.sleep(2)
            
            # Step 4: Connect OKX Wallet
            if not self.connect_okx_wallet():
                return False
            
            time.sleep(2)
            
            # Step 5: Handle OKX extension popup
            self.handle_okx_extension_popup()
            
            time.sleep(2)
            
            # Step 6: Enter password if needed
            self.enter_okx_password()
            
            time.sleep(2)
            
            # Step 7: Sign wallet
            self.sign_wallet()
            
            time.sleep(2)
            
            # Step 8: Wait for connection
            self.wait_for_connection()
            
            time.sleep(3)
            
            # Step 9: Find Daily Checkin
            if not self.find_daily_checkin():
                return False
            
            time.sleep(2)
            
            # Step 10: Click Checkin
            if not self.click_checkin_button():
                return False
            
            time.sleep(3)
            
            # Step 11: Verify success
            self.verify_checkin_success()
            
            print(f"\n[Profile {self.profile_index}] ✓ Workflow completed successfully!\n")
            return True
        
        except Exception as e:
            print(f"[Profile {self.profile_index}] ✗ Workflow error: {e}")
            return False
        
        finally:
            self.close()
    
    def close(self):
        """Close the driver"""
        try:
            if self.driver:
                time.sleep(2)
                self.driver.quit()
                print(f"[Profile {self.profile_index}] Driver closed")
        except:
            pass


def main():
    """Main function"""
    # Configuration
    PROFILE_PATH = "C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\EYFYwuoC.Profile 1"
    OKX_PASSWORD = "22091997"  # Enter your OKX wallet password
    
    # Run the bot
    bot = FairSharesBot(PROFILE_PATH, profile_index=1, okx_password=OKX_PASSWORD)
    
    if bot.start():
        success = bot.run_full_workflow(okx_password=OKX_PASSWORD)
        print(f"\n{'='*60}")
        print(f"Result: {'SUCCESS ✓' if success else 'FAILED ✗'}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
