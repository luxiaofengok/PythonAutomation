from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()

# Đường dẫn tới thư mục User Data (chung)
user_data_dir = r"C:\Users\Admin\AppData\Local\Google\Chrome\User Data"
options.add_argument(f"--user-data-dir={user_data_dir}")

# Chỉ định profile cụ thể (Default, Profile 1, Profile 2...)
options.add_argument("--profile-directory=Profile 1")

options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

# Bắt buộc Selenium mở trang bạn muốn
driver.get("https://www.facebook.com")

time.sleep(10)
driver.quit()
