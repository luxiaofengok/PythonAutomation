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
URL = "https://app.fairshares.io/waitlist"
METAMASK_PASSWORD = "22091997"

# ==================== SELECTORS ====================
CONNECT_WALLET_SELECTORS = [
    "//button[contains(., 'Connect Wallet')]",
    "//button[contains(., 'Kết nối ví')]",
]   

SIGN_MSG_SELECTORS = [
    "//button[contains(., 'Sign Message')]",    
    "//button[contains(., 'Sign message')]",
    "//button[contains(., 'Sign')]",
]
CLAIM_SELECTORS = [
    "//div[contains(., 'Daily NFT Check-in')]",
    "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[1]",
    "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/p[1]",
    "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div/div/button",
    "//button[contains(., 'Check in')]",
]

# ==================== HELPERS ====================

def _wait_for_new_window(driver, known_windows, timeout=15):
    """Chờ xuất hiện window mới ngoài known_windows, trả về handle hoặc None"""
    end = time.time() + timeout
    while time.time() < end:
        new_wins = [w for w in driver.window_handles if w not in known_windows]
        if new_wins:
            return new_wins[0]
        time.sleep(1)
    return None

def _click_metamask_buttons(driver, profile_index, step_label):
    """Click Connect/Sign/Confirm trong window hiện tại, trả về True nếu click được"""
    for selector in [
        "//button[contains(., 'Connect')]",
        "//button[contains(., 'Sign')]",
        "//button[contains(., 'Confirm')]",
    ]:
        btn = find_element_by_selectors(driver, [selector], wait_time=5)
        if btn:
            print(f"[Profile {profile_index}] [{step_label}] Click: {selector}")
            click_element_safe(driver, btn)
            time.sleep(3)
            return True
    print(f"[Profile {profile_index}] [{step_label}] Không thấy button nào để click")
    return False

# ==================== STEPS ====================

def access_and_connect(driver, profile_index):
    print(f"[Profile {profile_index}] [B1] Truy cập {URL}...")
    driver.get(URL)
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

def _handle_metamask_popup(driver, profile_index, main_window):
    """Xử lý popup Metamask: unlock → popup 1 → popup 2 (nếu có)"""

    # ---------- Popup 1 ----------
    popup1 = _wait_for_new_window(driver, known_windows={main_window}, timeout=15)
    if not popup1:
        print(f"[Profile {profile_index}] [B2] Không thấy popup MetaMask nào")
        driver.switch_to.window(main_window)
        return

    driver.switch_to.window(popup1)
    time.sleep(3)

    # Unlock nếu cần
    pass_el = find_element_by_selectors(driver, ["//input[@type='password']"], wait_time=3)
    if pass_el:
        print(f"[Profile {profile_index}] [B2] Unlock Metamask...")
        pass_el.send_keys(METAMASK_PASSWORD)
        time.sleep(1)
        unlock_btn = find_element_by_selectors(
            driver,
            ["//button[contains(., 'Unlock')]", "//button[contains(., 'Mở khóa')]"],
            wait_time=10
        )
        if unlock_btn:
            click_element_safe(driver, unlock_btn)
        time.sleep(3)

    # Click trong popup 1
    _click_metamask_buttons(driver, profile_index, "Popup1")

    # ---------- Popup 2 (confirm/sign) ----------
    # Chờ popup 2 xuất hiện — không dùng lại handle popup1 vì nó đã đóng
    popup2 = _wait_for_new_window(driver, known_windows={main_window}, timeout=10)
    if not popup2:
        print(f"[Profile {profile_index}] [B2] Không thấy popup 2 sau 10s → thử nhấn lại Connect Wallet + MetaMask rồi refresh...")
        # Switch về main
        if main_window in driver.window_handles:
            driver.switch_to.window(main_window)
        else:
            driver.switch_to.window(driver.window_handles[0])

        # Nhấn lại Connect Wallet nếu có
        connect_btn = find_element_by_selectors(driver, CONNECT_WALLET_SELECTORS, wait_time=5)
        if connect_btn:
            print(f"[Profile {profile_index}] [B2] Nhấn lại Connect Wallet...")
            click_element_safe(driver, connect_btn)
            time.sleep(3)

        # Nhấn lại MetaMask nếu có
        metamask_btn = find_element_by_selectors(driver, ["//button[contains(., 'MetaMask')]"], wait_time=5)
        if metamask_btn:
            print(f"[Profile {profile_index}] [B2] Nhấn lại MetaMask...")
            click_element_safe(driver, metamask_btn)
            time.sleep(3)

            # Xử lý lại popup 1
            retry_popup1 = _wait_for_new_window(driver, known_windows={main_window}, timeout=10)
            if retry_popup1:
                print(f"[Profile {profile_index}] [B2] Xử lý lại popup 1 trước khi reload...")
                driver.switch_to.window(retry_popup1)
                time.sleep(3)

                # Unlock nếu cần
                pass_el = find_element_by_selectors(driver, ["//input[@type='password']"], wait_time=3)
                if pass_el:
                    pass_el.send_keys(METAMASK_PASSWORD)
                    time.sleep(1)
                    unlock_btn = find_element_by_selectors(driver, ["//button[contains(., 'Unlock')]", "//button[contains(., 'Mở khóa')]"], wait_time=10)
                    if unlock_btn:
                        click_element_safe(driver, unlock_btn)
                    time.sleep(3)

                _click_metamask_buttons(driver, profile_index, "Popup1-Retry")
                time.sleep(3)

                # Switch về main sau popup 1
                if main_window in driver.window_handles:
                    driver.switch_to.window(main_window)
                else:
                    driver.switch_to.window(driver.window_handles[0])
            else:
                print(f"[Profile {profile_index}] [B2] Không thấy popup 1 retry, tiếp tục reload...")
                if main_window in driver.window_handles:
                    driver.switch_to.window(main_window)
                else:
                    driver.switch_to.window(driver.window_handles[0])

        # Reload
        print(f"[Profile {profile_index}] [B2] Reload web...")
        driver.refresh()
        time.sleep(5)
        # Chờ popup 2 xuất hiện sau reload
        popup2 = _wait_for_new_window(driver, known_windows={main_window}, timeout=15)

    if popup2:
        print(f"[Profile {profile_index}] [B2] Thấy popup 2, đang xử lý...")
        driver.switch_to.window(popup2)
        time.sleep(3)
        _click_metamask_buttons(driver, profile_index, "Popup2")
    else:
        print(f"[Profile {profile_index}] [B2] Vẫn không có popup 2 sau reload, tiếp tục...")

    # ---------- Switch về main ----------
    if main_window in driver.window_handles:
        driver.switch_to.window(main_window)
    else:
        driver.switch_to.window(driver.window_handles[0])
    time.sleep(5)

def handle_popups(driver, profile_index):
    main_window = driver.current_window_handle
    
    # Nhấn Metamask 
    metamask_btn = find_element_by_selectors(driver, ["//button[contains(., 'MetaMask')]"], wait_time=10)
    if not metamask_btn:
        print(f"[Profile {profile_index}] [B2] Không thấy MetaMask button sau 10s, skip B2")
        return False
    click_element_safe(driver, metamask_btn)
    time.sleep(5)

    # Xử lý popup Metamask
    _handle_metamask_popup(driver, profile_index, main_window)
    return True
    
def scroll_and_claim(driver, profile_index):
    # Bước 1: Tìm và nhấn Daily Tasks
    daily_btn = find_element_by_selectors(driver, [
        "//h3[contains(., 'Daily Tasks')]",
        "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div/h3[2]"
    ], wait_time=10)
    if not daily_btn:
        print(f"[Profile {profile_index}] Không tìm thấy Daily Tasks sau 10s")
        return False
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", daily_btn)
    time.sleep(3)
    click_element_safe(driver, daily_btn)
    time.sleep(3)

    # Bước 2: Tìm và nhấn Daily NFT Check-in (click vào row chứa text)
    nft_checkin_btn = find_element_by_selectors(driver, [
        # Leo lên div cha gần nhất từ thẻ p chứa text
        "//p[contains(text(), 'Daily NFT Check-in')]/..",
        "//p[contains(text(), 'Daily NFT Check-in')]/../../..",
        "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[1]",
    ], wait_time=8)
    if not nft_checkin_btn:
        print(f"[Profile {profile_index}] Không tìm thấy Daily NFT Check-in sau 10s")
        return False
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nft_checkin_btn)
    time.sleep(2)
    # Thử click bằng JS nếu click thường không ăn
    try:
        driver.execute_script("arguments[0].click();", nft_checkin_btn)
    except Exception:
        click_element_safe(driver, nft_checkin_btn)
    print(f"[Profile {profile_index}] Đã nhấn Daily NFT Check-in, chờ modal...")
    time.sleep(2)

    # Bước 3: Modal hiện ra → kiểm tra button là "Check in" hay "Mint"
    modal_btn = find_element_by_selectors(driver, [
        "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div/div/button",
        "/html/body/div/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div/div/button",
        "//button[contains(., 'Check in')]",
        "//button[contains(., 'Mint')]",
    ], wait_time=5)
    if not modal_btn:
        print(f"[Profile {profile_index}] Không tìm thấy nút trong modal sau 5s")
        return False

    btn_text = modal_btn.text.strip()
    print(f"[Profile {profile_index}] Thấy button modal: '{btn_text}'")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", modal_btn)
    time.sleep(2)

    # ---------- Trường hợp 1: Check in ----------
    if "Check in" in btn_text or "Check In" in btn_text:
        click_element_safe(driver, modal_btn)
        print(f"[Profile {profile_index}] Đã nhấn Check in!")
        time.sleep(20)
        return True

    # ---------- Trường hợp 2: Mint ----------
    elif "Mint" in btn_text:
        main_window = driver.current_window_handle
        click_element_safe(driver, modal_btn)
        print(f"[Profile {profile_index}] Đã nhấn Mint, chờ popup MetaMask confirm...")

        # Chờ popup MetaMask confirm xuất hiện
        mint_popup = _wait_for_new_window(driver, known_windows={main_window}, timeout=20)
        if not mint_popup:
            print(f"[Profile {profile_index}] Không thấy popup confirm sau 20s")
            return False

        driver.switch_to.window(mint_popup)
        time.sleep(3)

        # Nhấn Confirm trong popup MetaMask
        confirm_btn = find_element_by_selectors(driver, [
            "//button[contains(., 'Confirm')]",
            "//button[contains(., 'Xác nhận')]",
        ], wait_time=10)
        if confirm_btn:
            click_element_safe(driver, confirm_btn)
            print(f"[Profile {profile_index}] Đã nhấn Confirm mint NFT!")
        else:
            print(f"[Profile {profile_index}] Không thấy nút Confirm trong popup")

        time.sleep(3)

        # Tắt popup MetaMask (đóng window)
        try:
            driver.close()
            print(f"[Profile {profile_index}] Đã đóng popup MetaMask")
        except Exception:
            pass
        time.sleep(2)

        # Switch về main window
        if main_window in driver.window_handles:
            driver.switch_to.window(main_window)
        else:
            driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)

        # Nhấn Done trong modal
        done_btn = find_element_by_selectors(driver, [
            "/html/body/div/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div/div/div[5]/button[2]",
            "//button[contains(., 'Done')]",
        ], wait_time=15)
        if done_btn:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", done_btn)
            time.sleep(2)
            click_element_safe(driver, done_btn)
            print(f"[Profile {profile_index}] Đã nhấn Done!")
        else:
            print(f"[Profile {profile_index}] Không thấy nút Done, bỏ qua")

        time.sleep(10)
        return True

    else:
        print(f"[Profile {profile_index}] Button không xác định: '{btn_text}', bỏ qua")
        return False

def run_fairshare(profile_path, profile_index):
    driver = None
    
    try:
        print(f"\n[Profile {profile_index}] Starting Fairshare automation...")
        driver = create_firefox_driver(profile_path)

        if not access_and_connect(driver, profile_index):
            print(f"[Profile {profile_index}] Failed at access/connect step.")
            return False
        
        if not handle_popups(driver, profile_index):
            print(f"[Profile {profile_index}] Failed at handling popups step.")
            return False
        
        if not scroll_and_claim(driver, profile_index):
            print(f"[Profile {profile_index}] Failed at scroll/claim step.")
            return False
        
        print(f"[Profile {profile_index}] Fairshare automation completed successfully!")
        return True

    except Exception as e:
        print(f"\n[Profile {profile_index}] [ERROR] An error occurred: {str(e)}\n")
        return False
    
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


if __name__ == "__main__":
    results = run_all_batches(run_fairshare, FIREFOX_PROFILES)
    # result = run_fairshare(FIREFOX_PROFILES[1])