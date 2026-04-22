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
URL = "https://portal.stormrae.ai/"
PHANTOM_PASSWORD = "22091997"

# ==================== SELECTORS ====================
CONNECT_WALLET_SELECTORS = [
    "/html/body/div[5]/main/div/div/div[2]/div/div[3]/div/div/button",
    "//button[contains(., 'Connect Wallet')]",
]
SIGN_MSG_SELECTORS = [
    "//button[contains(., 'Sign Message')]",
    "//button[contains(., 'Sign message')]",
]
CLAIM_SELECTORS = [
    "/html/body/div[5]/main/div/div/div[5]/div/div/div[3]/div[2]/div/div[4]/div[1]/button",
    "//button[contains(@class, 'group/taskbtn')]",
    "//button[contains(@class, 'taskbtn')]",
    "//button[span[contains(text(), 'Claim')]]",
    "//button[contains(., 'Claim') and not(contains(., 'Auto'))]",
]


# ==================== B1: VÀO WEB + NHẤN CONNECT ====================
def access_and_connect(driver, profile_index):
    print(f"[Profile {profile_index}] [B1] Truy cập {URL}...")
    driver.get(URL)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)
    driver.refresh()
    time.sleep(15)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)

    connect_btn = find_element_by_selectors(driver, CONNECT_WALLET_SELECTORS, wait_time=15)
    if not connect_btn:
        print(f"[Profile {profile_index}] [B1] Không thấy Connect Wallet sau 15s → đã login sẵn, skip B2")
        return scroll_and_claim(driver, profile_index)

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
    phantom_btn = find_element_by_selectors(driver, ["//button[contains(., 'Phantom')]"], wait_time=10)
    if not phantom_btn:
        print(f"[Profile {profile_index}] [B2] Không tìm thấy nút Phantom.")
        return False
    click_element_safe(driver, phantom_btn)

    # Chờ popup tối đa 8s
    try:
        WebDriverWait(driver, 8).until(lambda d: len(d.window_handles) > 1)
        print(f"[Profile {profile_index}] [B2] Popup xuất hiện, đang xử lý...")
        _handle_phantom_popup(driver, profile_index, main_window)

    except Exception:
        # Không có popup → reload → Connect → rồi chia 2 trường hợp
        print(f"[Profile {profile_index}] [B2] Không thấy popup sau 8s, reload...")
        driver.refresh()
        time.sleep(5)

        # Nhấn Connect Wallet
        connect_btn = find_element_by_selectors(driver, CONNECT_WALLET_SELECTORS, wait_time=10)
        if connect_btn:
            print(f"[Profile {profile_index}] [B2] Nhấn Connect Wallet sau reload...")
            click_element_safe(driver, connect_btn)
            time.sleep(2)

        # TH1: Phantom button hiện → nhấn Phantom → xử lý popup
        phantom_btn2 = find_element_by_selectors(driver, ["//button[contains(., 'Phantom')]"], wait_time=5)
        if phantom_btn2:
            print(f"[Profile {profile_index}] [B2] Thấy Phantom button, nhấn...")
            click_element_safe(driver, phantom_btn2)
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
            _handle_phantom_popup(driver, profile_index, main_window)

        else:
            # TH2: Không thấy Phantom → nhấn Sign Message → xử lý popup
            sign_btn = find_element_by_selectors(driver, SIGN_MSG_SELECTORS, wait_time=10)
            if not sign_btn:
                print(f"[Profile {profile_index}] [B2] Không tìm thấy Phantom lẫn Sign Message.")
                return False
            print(f"[Profile {profile_index}] [B2] Thấy Sign Message, nhấn...")
            click_element_safe(driver, sign_btn)
            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
            _handle_phantom_popup(driver, profile_index, main_window)

    sign_btn = find_element_by_selectors(driver, SIGN_MSG_SELECTORS, wait_time=10)
    if sign_btn:
        click_element_safe(driver, sign_btn)
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        _handle_phantom_popup(driver, profile_index, main_window)

    print(f"[Profile {profile_index}] [B2] Connect thành công, về dashboard")
    return True


# ==================== CHECK DASHBOARD ====================
def check_dashboard(driver, profile_index):
    """Kiểm tra xem đã vào dashboard thành công chưa bằng URL"""
    try:
        current_url = driver.current_url
        if "/dashboard" in current_url:
            print(f"[Profile {profile_index}] ✅ Đã vào dashboard")
            return True
        else:
            print(f"[Profile {profile_index}] ❌ Chưa vào dashboard (URL: {current_url})")
            return False
        
    except Exception as e:
        print(f"[Profile {profile_index}] ❌ Lỗi kiểm tra dashboard: {str(e)}")
        return False


# ==================== B3: SCROLL TÌM VÀ NHẤN CLAIM ====================
def scroll_and_claim(driver, profile_index):
    connected_indicator = find_element_by_selectors(driver, ["//div[contains(text(), 'Continue')]", "/html/body/div[5]/main/div/div/div[3]/div/button"], wait_time=10)
    if connected_indicator:
        click_element_safe(driver, connected_indicator)
        time.sleep(5)

    print(f"[Profile {profile_index}] [B3] Scroll tìm nút Claim...")
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

    for i in range(20):
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(0.5)

        claim_btn = find_element_by_selectors(driver, CLAIM_SELECTORS, wait_time=1)
        if claim_btn:
            print(f"[Profile {profile_index}] [B3] Thấy Claim sau {i * 300}px")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", claim_btn)
            time.sleep(3)

            # Dùng đúng XPath qua JS như test trên console
            try:
                driver.execute_script("""
                    var btn = document.evaluate(
                        "/html/body/div[5]/main/div/div/div[5]/div/div/div[3]/div[2]/div/div[4]/div[1]/button",
                        document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null
                    ).singleNodeValue;
                    if (btn) { btn.click(); }
                """)
                print(f"[Profile {profile_index}] [B3] Đã nhấn Claim (XPath JS)")
            except Exception as e:
                print(f"[Profile {profile_index}] [B3] Lỗi: {str(e)}")

            time.sleep(8)


            print(f"[Profile {profile_index}] [B3] Claim thành công ✅")
            return True

    print(f"[Profile {profile_index}] [B3] Không tìm thấy nút Claim.")
    return False


# ==================== MAIN FLOW ====================
def run_profile(profile_path, profile_index):
    driver = None
    try:
        print(f"\n[Profile {profile_index}] Khởi động Firefox...")
        driver = create_firefox_driver(profile_path)

        if not access_and_connect(driver, profile_index):
            return False
        
        # Handle Phantom với retry nếu chưa vào dashboard
        max_retries = 2
        for retry in range(max_retries):
            print(f"[Profile {profile_index}] [B2] Lần thử {retry + 1}/{max_retries}")
            if not handle_phantom(driver, profile_index):
                return False
            
            # Check xem đã vào dashboard chưa
            time.sleep(3)
            if check_dashboard(driver, profile_index):
                break
            
            if retry < max_retries - 1:
                print(f"[Profile {profile_index}] [B2] Dashboard chưa load, thử lại...")
                time.sleep(2)
        
        if not scroll_and_claim(driver, profile_index):
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
    run_all_batches(run_profile, FIREFOX_PROFILES)
    # run_profile(FIREFOX_PROFILES[1], 2)  # Chạy riêng profile đầu tiên để debug

if __name__ == "__main__":
    main()