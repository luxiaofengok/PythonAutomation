# open_profile_with_extensions.py
import os
import shutil
import subprocess
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

ORIG_USER_DATA = r"C:\Users\Admin\AppData\Local\Google\Chrome\User Data"
PROFILE_NAME = "Profile 1"  # tên profile nguồn
TARGET_ROOT = r"C:\selenium_profiles\profile_with_ext"  # nơi lưu bản sao
URL = "https://www.facebook.com"
WAIT_TIMEOUT = 20

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)
    return p

def kill_chrome():
    """Kill all Chrome processes to ensure profile is not locked"""
    try:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Closed existing Chrome instances")
    except Exception:
        pass

def copy_profile_with_extensions(src_user_data, profile_name, target_root):
    """Copy profile including Extensions folder, skip locked files"""
    src = os.path.join(src_user_data, profile_name)
    if not os.path.isdir(src):
        raise FileNotFoundError(f"Source profile not found: {src}")
    ensure_dir(target_root)
    tgt = os.path.join(target_root, profile_name)
    
    # Always remove old copy and create fresh one
    if os.path.exists(tgt):
        print(f"Removing old profile copy...")
        shutil.rmtree(tgt, ignore_errors=True)
        time.sleep(0.5)
    
    print("Copying profile (including Extensions - may take time)...")
    
    # Manual copy with error handling
    def copy_with_skip(src_dir, dst_dir):
        """Recursively copy directory, skip locked files"""
        os.makedirs(dst_dir, exist_ok=True)
        skipped = 0
        copied = 0
        
        for item in os.listdir(src_dir):
            src_path = os.path.join(src_dir, item)
            dst_path = os.path.join(dst_dir, item)
            
            try:
                if os.path.isdir(src_path):
                    s, c = copy_with_skip(src_path, dst_path)
                    skipped += s
                    copied += c
                else:
                    shutil.copy2(src_path, dst_path)
                    copied += 1
            except (PermissionError, OSError) as e:
                skipped += 1
            except Exception as e:
                skipped += 1
        
        return skipped, copied
    
    skipped, copied = copy_with_skip(src, tgt)
    print(f"✓ Profile copied: {copied} files copied, {skipped} files skipped")
    
    return tgt

def main():
    # 1) Ensure Chrome is completely closed
    kill_chrome()
    time.sleep(3)
    
    # 2) Copy profile with extensions
    try:
        copied_profile = copy_profile_with_extensions(ORIG_USER_DATA, PROFILE_NAME, TARGET_ROOT)
        print(f"✓ Profile ready at: {copied_profile}")
    except Exception as e:
        print("⚠️ Profile copy had issues but continuing:", e)
    
    # 3) Launch Chrome with the copied profile (WITH extensions)
    opts = Options()
    opts.add_argument(f"--user-data-dir={TARGET_ROOT}")
    opts.add_argument(f"--profile-directory={PROFILE_NAME}")
    # NOTE: NOT disabling extensions - they will load normally
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
        print("✅ Chrome launched with extensions enabled")
    except Exception as e:
        print("❌ Failed to start Chrome via Selenium:", e)
        sys.exit(1)
    
    driver.get(URL)
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.title_contains("Facebook"))
        print("✅ Facebook page loaded successfully")
    except Exception:
        print("⚠️ Page did not confirm title within timeout; check browser manually.")
    
    # Keep browser open for interaction - press Ctrl+C to quit
    print("\n⚠️ Browser will stay open. Close manually or press Ctrl+C to quit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n✓ Closing browser...")
        driver.quit()
        print("ℹ️ Done. Original profile untouched.")

if __name__ == "__main__":
    main()
