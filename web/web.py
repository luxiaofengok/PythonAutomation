# open_profile84_noext.py
import os
import shutil
import subprocess
import time
import sys
import sqlite3
import logging
from datetime import datetime, timedelta
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
URL = "https://www.youtube.com"
WAIT_TIMEOUT = 20

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)
    return p

def save_browser_history_to_log(profile_dir, log_file="browser_history.log"):
    """Đọc lịch sử từ Chrome History database và lưu vào file log"""
    history_db = os.path.join(profile_dir, "History")
    
    if not os.path.exists(history_db):
        print(f"⚠️ History database not found at {history_db}")
        return
    
    # Copy History file tạm vì Chrome đang lock nó
    temp_history = os.path.join(os.path.dirname(log_file), "temp_history")
    try:
        shutil.copy2(history_db, temp_history)
    except Exception as e:
        print(f"⚠️ Could not copy history: {e}")
        return
    
    try:
        conn = sqlite3.connect(temp_history)
        cursor = conn.cursor()
        
        # Lấy lịch sử truy cập từ bảng urls
        query = """
            SELECT url, title, visit_count, last_visit_time 
            FROM urls 
            ORDER BY last_visit_time DESC 
            LIMIT 100
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Ghi vào file log
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write(f"BROWSER HISTORY LOG - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            for idx, (url, title, visit_count, last_visit) in enumerate(results, 1):
                # Chrome's timestamp is in microseconds since 1601-01-01
                # Convert to readable format
                if last_visit:
                    chrome_time = datetime(1601, 1, 1) + timedelta(microseconds=last_visit)
                    time_str = chrome_time.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    time_str = "N/A"
                
                f.write(f"{idx}. [{time_str}] (Visits: {visit_count})\n")
                f.write(f"   Title: {title or 'No title'}\n")
                f.write(f"   URL: {url}\n\n")
        
        conn.close()
        print(f"✅ History saved to {log_file}")
        
    except Exception as e:
        print(f"❌ Error reading history: {e}")
    finally:
        # Xóa file tạm
        if os.path.exists(temp_history):
            os.remove(temp_history)

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
    opts.add_argument("--headless=new")  # Chạy headless mode
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    # Setup logging
    log_file = os.path.join(os.getcwd(), "selenium_run.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    try:
        logging.info("🚀 Starting Chrome in headless mode...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=opts)
        logging.info("✅ Chrome driver initialized successfully")
    except Exception as e:
        logging.error(f"❌ Failed to start Chrome via Selenium: {e}")
        sys.exit(1)

    try:
        logging.info(f"🌐 Navigating to {URL}...")
        driver.get(URL)
        logging.info(f"📄 Current URL: {driver.current_url}")
        logging.info(f"📋 Page title: {driver.title}")
        
        # Take screenshot
        screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
        driver.save_screenshot(screenshot_path)
        logging.info(f"📸 Screenshot saved to {screenshot_path}")
        
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.title_contains("Facebook"))
        logging.info("✅ Facebook page loaded successfully in headless mode")
    except Exception as e:
        logging.warning(f"⚠️ Page load issue: {e}")
        logging.info(f"Current title: {driver.title}")

    # Keep browser running in background until user presses Enter
    print("\n" + "="*60)
    print("🌐 Browser is running in HEADLESS mode.")
    print(f"📝 Check logs at: {log_file}")
    print(f"📸 Screenshot saved at: screenshot.png")
    print("   Press ENTER here to close and save history log...")
    print("="*60)
    input()
    
    logging.info("🛑 Closing browser...")
    driver.quit()
    logging.info("✅ Browser closed")
    
    # Save browser history to log file
    history_log = os.path.join(os.getcwd(), "browser_history.log")
    logging.info("💾 Saving browser history...")
    save_browser_history_to_log(TARGET_PROFILE_DIR, history_log)
    logging.info(f"✅ History saved to {history_log}")
    
    print("\nℹ️ Done! Check these files:")
    print(f"  📝 Run log: {log_file}")
    print(f"  📜 History: {history_log}")
    print(f"  📸 Screenshot: screenshot.png")

if __name__ == "__main__":
    main()