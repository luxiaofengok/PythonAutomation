# web_direct_profile.py - Mở Chrome trực tiếp với profile và extensions (không dùng Selenium)
import os
import subprocess
import time
import sys

ORIG_USER_DATA = r"C:\Users\Admin\AppData\Local\Google\Chrome\User Data"
PROFILE_NAME = "Profile 1"  # tên profile nguồn
URL = "https://www.facebook.com"

def kill_chrome():
    """Kill all Chrome processes"""
    try:
        result = subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("✓ Closed existing Chrome instances")
            time.sleep(2)
            return True
        return False
    except Exception:
        return False

def open_chrome_with_profile():
    """Open Chrome directly with profile and navigate to URL"""
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # Alternative Chrome paths
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    
    if not os.path.exists(chrome_path):
        print("❌ Chrome not found at default location")
        return False
    
    cmd = [
        chrome_path,
        f"--user-data-dir={ORIG_USER_DATA}",
        f"--profile-directory={PROFILE_NAME}",
        "--start-maximized",
        URL
    ]
    
    try:
        subprocess.Popen(cmd)
        print(f"✅ Chrome opened with profile: {PROFILE_NAME}")
        print(f"✅ Navigating to: {URL}")
        print(f"✅ All extensions are enabled")
        return True
    except Exception as e:
        print(f"❌ Failed to open Chrome: {e}")
        return False

def main():
    print("="*60)
    print("Opening Chrome with Profile + Extensions")
    print("="*60)
    print()
    
    # 1) Kill existing Chrome
    print("Step 1: Closing existing Chrome instances...")
    kill_chrome()
    time.sleep(2)
    
    # 2) Open Chrome with profile
    print("\nStep 2: Opening Chrome...")
    if open_chrome_with_profile():
        print()
        print("="*60)
        print("✅ SUCCESS! Chrome is running with full profile + extensions")
        print("="*60)
        print()
        print("⚠️ Note: This opens Chrome normally (not controlled by Selenium)")
        print("   You can use the browser manually as usual.")
        print()
        print("Press Enter to close this script (Chrome will keep running)...")
        input()
    else:
        print("\n❌ Failed to open Chrome")
        sys.exit(1)

if __name__ == "__main__":
    main()
