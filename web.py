# open_profile84_noext.py
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
PROFILE_NAME = "Profile 84"                              # tên profile nguồn
TARGET_ROOT = r"C:\selenium_profiles\profile84_noext"    # nơi lưu bản sao
TARGET_PROFILE_DIR = os.path.join(TARGET_ROOT, PROFILE_NAME)
URL = "https://www.facebook.com"
WAIT_TIMEOUT = 20

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)
    return p

def kill_chrome():
    try:
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def copy_profile_no_extensions(src_user_data, profile_name, target_root):
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
    
    # Function to ignore Extensions folder during copy
    def ignore_extensions(dir, files):
        if os.path.basename(dir) == profile_name:
            # Ignore Extensions folder at root level of profile
            return {'Extensions'} if 'Extensions' in files else set()
        return set()
    
    print("Copying profile (skipping Extensions folder)...")
    shutil.copytree(src, tgt, ignore=ignore_extensions)
    print("✓ Profile copied successfully (Extensions folder skipped)")
    return tgt

def main():
    # 1) Ensure Chrome closed so copy/launch can work reliably
    kill_chrome()
    time.sleep(2)  # Wait longer for Chrome to fully close

    # 2) copy profile (skip if exists)
    try:
        copied_profile = copy_profile_no_extensions(ORIG_USER_DATA, PROFILE_NAME, TARGET_ROOT)
    except Exception as e:
        print("❌ Error copying profile:", e)
        sys.exit(1)

    # 3) Launch Chrome using the copied profile with extensions disabled
    opts = Options()
    opts.add_argument(f"--user-data-dir={TARGET_ROOT}")
    opts.add_argument(f"--profile-directory={PROFILE_NAME}")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")
    opts.add_argument("--start-maximized")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
    except Exception as e:
        print("❌ Failed to start Chrome via Selenium:", e)
        sys.exit(1)

    driver.get(URL)
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.title_contains("Facebook"))
        print("✅ Facebook page loaded in profile copy (extensions disabled).")
    except Exception:
        print("⚠️ Page did not confirm title within timeout; check browser manually.")

    # keep open briefly for visual confirmation, then quit
    time.sleep(5)
    driver.quit()  
    print("ℹ️ Done. Browser closed; original profile untouched.")

if __name__ == "__main__":
    main()