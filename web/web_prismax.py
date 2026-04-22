from web_source import (
    create_firefox_driver,
    find_element_by_selectors,
    click_element_safe,
    FIREFOX_PROFILES,
    run_all_batches
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# ==================== CONFIGURATION ====================
URL = "https://app.prismax.ai/"
PHANTOM_PASSWORD = "22091997"

# ==================== SELECTORS ====================
CONNECT_WALLET_SELECTORS = [
    # "//button[contains(., 'Connect Wallet')]",
    # "//button[contains(., 'Connect')]",
    # "/html/body/div[1]/div/div[3]/div[1]/div/div/div[2]",
    # "//div[contains(@class, 'Connect')]",
    "//div[contains(@class, 'ConnectWalletHeader_userIcon__oJgYB undefined')]",
]
SIGN_MSG_SELECTORS = [
    "//button[contains(., 'Sign Message')]",
    "//button[contains(., 'Sign message')]"
]

# ==================== B1: VÀO WEB + NHẤN CONNECT ====================
def access_and_connect(driver, profile_index):
    print(f"[Profile {profile_index}] [B1] Truy cập {URL}...")
    driver.get(URL)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(8)
    driver.refresh()
    time.sleep(15)
    driver.refresh()
    time.sleep(15)

    connect_btn = find_element_by_selectors(driver, CONNECT_WALLET_SELECTORS, wait_time=15)
    if not connect_btn:
        print(f"[Profile {profile_index}] [B1] Không thấy Connect Wallet sau 15s → đã login sẵn, skip B2")
        return driver.refresh()  # Refresh để load lại trang sau khi đã login sẵn

    print(f"[Profile {profile_index}] [B1] Thấy Connect Wallet, đang nhấn...")
    click_element_safe(driver, connect_btn)
    time.sleep(5)
    return True
# ==================== B2: XỬ LÝ PHANTOM ====================
def _handle_phantom_popup(driver, profile_index, main_window):
    """Xử lý popup Phantom: unlock nếu cần, nhấn Connect/Sign/Approve"""
    new_window = [w for w in driver.window_handles if w != main_window][0]
    driver.switch_to.window(new_window)
    time.sleep(3)

    # Unlock nếu cần
    pass_el = find_element_by_selectors(driver, ["//input[@type='password']"], wait_time=3)
    if pass_el:
        print(f"[Profile {profile_index}] [B2] Unlock Phantom...")
        pass_el.send_keys(PHANTOM_PASSWORD)
        time.sleep(1)
        unlock_btn = find_element_by_selectors(driver, ["//button[contains(., 'Unlock')]","//button[contains(., 'Mở khóa')]"], wait_time=10)
        if unlock_btn:
            click_element_safe(driver, unlock_btn)
        time.sleep(2)

    # Nhấn Connect / Sign / Confirm
    for selector in ["//button[contains(., 'Connect')]", "//button[contains(., 'Xác nhận')]", "//button[contains(., 'Confirm')]"]:
        btn = find_element_by_selectors(driver, [selector], wait_time=5)
        if btn:
            click_element_safe(driver, btn)
            break

    time.sleep(3)
    driver.switch_to.window(main_window)
    time.sleep(5)

def handle_phantom(driver, profile_index):
    main_window = driver.current_window_handle

    # Nhấn Phantom
    phantom_btn = find_element_by_selectors(driver, ["//button[contains(., 'Phantom')]", "/html/body/div[1]/div/div[3]/div[1]/div/div/div[4]/div[3]"], wait_time=10)
    if not phantom_btn:
        print(f"[Profile {profile_index}] [B2] Không tìm thấy nút Phantom.")
        return False
    click_element_safe(driver, phantom_btn)

    try:
        WebDriverWait(driver, 8).until(lambda d: len(d.window_handles) > 1)
        print(f"[Profile {profile_index}] [B2] Popup xuất hiện, đang xử lý...")
        _handle_phantom_popup(driver, profile_index, main_window)

    except Exception as e:
        driver.refresh()
        print(f"[Profile {profile_index}] [B2] Lỗi xử lý popup Phantom: {str(e)}. Đã refresh trang.")
        time.sleep(5)
        click_element_safe(driver, phantom_btn)
        time.sleep(2)
        _handle_phantom_popup(driver, profile_index, main_window)
        driver.refresh()
        print(f"[Profile {profile_index}] [B2] Đã refresh lại trang sau khi xử lý Phantom.")
        time.sleep(8)
    return True


# ==================== MAIN FUNCTION ====================
def run_prismax(profile_path, profile_index):
    driver = None
    try:
        print(f"\n[Profile {profile_index}] Khởi động Firefox...")
        driver = create_firefox_driver(profile_path)

        if not access_and_connect(driver, profile_index):
            return False
        if not handle_phantom(driver, profile_index):
            return False

        print(f"[Profile {profile_index}] ✅ Hoàn thành")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] ❌ Lỗi: {str(e)}")
        return False

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


def main():
    run_all_batches(run_prismax, FIREFOX_PROFILES)
    # run_prismax(FIREFOX_PROFILES[0], 1)
    

if __name__ == "__main__":
    main()