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
        time.sleep(2)
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

def _is_logged_in(driver, profile_index, timeout=15):
    """Kiểm tra đã vào được dashboard chưa (không còn thấy Connect Wallet)"""
    print(f"[Profile {profile_index}] Kiểm tra login thành công...")
    end = time.time() + timeout
    while time.time() < end:
        connect_btn = find_element_by_selectors(driver, CONNECT_WALLET_SELECTORS, wait_time=5)
        if not connect_btn:
            print(f"[Profile {profile_index}] Login thanh cong, vao duoc dashboard")
            return True
        time.sleep(2)
    print(f"[Profile {profile_index}] Van thay Connect Wallet sau {timeout}s → chua login")
    return False

def _handle_popup1(driver, profile_index, main_window, label="Popup1"):
    """Xử lý 1 popup MetaMask: unlock nếu cần rồi click"""
    popup = _wait_for_new_window(driver, known_windows={main_window}, timeout=10)
    if not popup:
        print(f"[Profile {profile_index}] [{label}] Không thấy popup")
        return False

    driver.switch_to.window(popup)
    time.sleep(5)

    pass_el = find_element_by_selectors(driver, ["//input[@type='password']"], wait_time=3)
    if pass_el:
        print(f"[Profile {profile_index}] [{label}] Unlock Metamask...")
        pass_el.send_keys(METAMASK_PASSWORD)
        time.sleep(1)
        unlock_btn = find_element_by_selectors(
            driver,
            ["//button[contains(., 'Unlock')]", "//button[contains(., 'Mo khoa')]"],
            wait_time=10
        )
        if unlock_btn:
            click_element_safe(driver, unlock_btn)
        time.sleep(3)

    _click_metamask_buttons(driver, profile_index, label)
    return True

# ==================== STEPS ====================

def access_and_connect(driver, profile_index):
    print(f"[Profile {profile_index}] [B1] Truy cap {URL}...")
    driver.get(URL)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(8)

    driver.refresh()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(8)

    driver.refresh()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(8)

    connect_btn = find_element_by_selectors(driver, CONNECT_WALLET_SELECTORS, wait_time=15)
    if not connect_btn:
        print(f"[Profile {profile_index}] [B1] Khong thay Connect Wallet → da login san, skip B2")
        return scroll_and_claim(driver, profile_index)

    print(f"[Profile {profile_index}] [B1] Thay Connect Wallet, dang nhan...")
    click_element_safe(driver, connect_btn)
    time.sleep(5)
    return True

def _handle_metamask_popup(driver, profile_index, main_window):
    """Xu ly popup Metamask: unlock → popup 1 → popup 2 → verify login, retry neu can"""

    # ---------- Popup 1 ----------
    popup1 = _wait_for_new_window(driver, known_windows={main_window}, timeout=15)
    if not popup1:
        print(f"[Profile {profile_index}] [B2] Khong thay popup MetaMask nao")
        if main_window in driver.window_handles:
            driver.switch_to.window(main_window)
        return False

    driver.switch_to.window(popup1)
    time.sleep(3)

    pass_el = find_element_by_selectors(driver, ["//input[@type='password']"], wait_time=3)
    if pass_el:
        print(f"[Profile {profile_index}] [B2] Unlock Metamask...")
        pass_el.send_keys(METAMASK_PASSWORD)
        time.sleep(1)
        unlock_btn = find_element_by_selectors(
            driver,
            ["//button[contains(., 'Unlock')]", "//button[contains(., 'Mo khoa')]"],
            wait_time=10
        )
        if unlock_btn:
            click_element_safe(driver, unlock_btn)
        time.sleep(3)

    _click_metamask_buttons(driver, profile_index, "Popup1")

    # ---------- Popup 2 ----------
    popup2 = _wait_for_new_window(driver, known_windows={main_window}, timeout=10)
    if not popup2:
        print(f"[Profile {profile_index}] [B2] Khong thay popup 2 sau 10s → nhan lai Connect Wallet + MetaMask roi refresh...")

        if main_window in driver.window_handles:
            driver.switch_to.window(main_window)
        else:
            driver.switch_to.window(driver.window_handles[0])

        connect_btn = find_element_by_selectors(driver, CONNECT_WALLET_SELECTORS, wait_time=5)
        if connect_btn:
            print(f"[Profile {profile_index}] [B2] Nhan lai Connect Wallet...")
            click_element_safe(driver, connect_btn)
            time.sleep(3)

        metamask_btn = find_element_by_selectors(driver, ["//button[contains(., 'MetaMask')]"], wait_time=5)
        if metamask_btn:
            print(f"[Profile {profile_index}] [B2] Nhan lai MetaMask...")
            click_element_safe(driver, metamask_btn)
            time.sleep(3)

            retry_popup1 = _wait_for_new_window(driver, known_windows={main_window}, timeout=10)
            if retry_popup1:
                print(f"[Profile {profile_index}] [B2] Xu ly lai popup 1 truoc khi reload...")
                driver.switch_to.window(retry_popup1)
                time.sleep(3)

                pass_el = find_element_by_selectors(driver, ["//input[@type='password']"], wait_time=3)
                if pass_el:
                    pass_el.send_keys(METAMASK_PASSWORD)
                    time.sleep(1)
                    unlock_btn = find_element_by_selectors(driver, ["//button[contains(., 'Unlock')]", "//button[contains(., 'Mo khoa')]"], wait_time=10)
                    if unlock_btn:
                        click_element_safe(driver, unlock_btn)
                    time.sleep(3)

                _click_metamask_buttons(driver, profile_index, "Popup1-Retry")
                time.sleep(3)

            if main_window in driver.window_handles:
                driver.switch_to.window(main_window)
            else:
                driver.switch_to.window(driver.window_handles[0])

        print(f"[Profile {profile_index}] [B2] Reload web...")
        driver.refresh()
        time.sleep(5)
        popup2 = _wait_for_new_window(driver, known_windows={main_window}, timeout=15)

    if popup2:
        print(f"[Profile {profile_index}] [B2] Thay popup 2, dang xu ly...")
        driver.switch_to.window(popup2)
        time.sleep(3)
        _click_metamask_buttons(driver, profile_index, "Popup2")
    else:
        print(f"[Profile {profile_index}] [B2] Van khong co popup 2 sau reload, tiep tuc...")

    # Switch ve main
    if main_window in driver.window_handles:
        driver.switch_to.window(main_window)
    else:
        driver.switch_to.window(driver.window_handles[0])
    time.sleep(10)

    # ---------- Kiem tra login thanh cong ----------
    if _is_logged_in(driver, profile_index, timeout=15):
        return  # OK, tiep tuc

    # Chua login → lam lai flow popup 1 + popup 2
    print(f"[Profile {profile_index}] [B2] Chua login → thuc hien lai flow popup...")

    connect_btn = find_element_by_selectors(driver, CONNECT_WALLET_SELECTORS, wait_time=5)
    if connect_btn:
        click_element_safe(driver, connect_btn)
        time.sleep(3)

    metamask_btn = find_element_by_selectors(driver, ["//button[contains(., 'MetaMask')]"], wait_time=5)
    if metamask_btn:
        click_element_safe(driver, metamask_btn)
        time.sleep(3)

    _handle_popup1(driver, profile_index, main_window, label="Popup1-LoginRetry")

    if main_window in driver.window_handles:
        driver.switch_to.window(main_window)
    else:
        driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

    popup2_retry = _wait_for_new_window(driver, known_windows={main_window}, timeout=15)
    if popup2_retry:
        print(f"[Profile {profile_index}] [B2] Thay popup 2 retry, dang xu ly...")
        driver.switch_to.window(popup2_retry)
        time.sleep(3)
        _click_metamask_buttons(driver, profile_index, "Popup2-LoginRetry")
    else:
        print(f"[Profile {profile_index}] [B2] Khong thay popup 2 retry")

    if main_window in driver.window_handles:
        driver.switch_to.window(main_window)
    else:
        driver.switch_to.window(driver.window_handles[0])
    time.sleep(10)

def handle_popups(driver, profile_index):
    main_window = driver.current_window_handle

    metamask_btn = find_element_by_selectors(driver, ["//button[contains(., 'MetaMask')]"], wait_time=10)
    if not metamask_btn:
        print(f"[Profile {profile_index}] [B2] Khong thay MetaMask button sau 10s, skip B2")
        return False
    click_element_safe(driver, metamask_btn)
    time.sleep(5)

    _handle_metamask_popup(driver, profile_index, main_window)
    return True

def scroll_and_claim(driver, profile_index):
    # Buoc 1: Tim va nhan Daily Tasks
    daily_btn = find_element_by_selectors(driver, [
        "//h3[contains(., 'Daily Tasks')]",
        "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div/h3[2]"
    ], wait_time=10)
    if not daily_btn:
        print(f"[Profile {profile_index}] Khong tim thay Daily Tasks sau 10s")
        return False
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", daily_btn)
    time.sleep(3)
    click_element_safe(driver, daily_btn)
    time.sleep(3)
    
    main_window = driver.current_window_handle
    like_btn = find_element_by_selectors(driver, [
        "/html/body/div[3]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/p[2]",
        "//p[contains(., 'Like on X')]",
    ], wait_time=10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", like_btn)
    if like_btn:
        print(f"[Profile {profile_index}] Nhan like tren X...")
        click_element_safe(driver, like_btn)
        time.sleep(3)
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            time.sleep(2)
            driver.close()
    driver.switch_to.window(main_window)
    time.sleep(3)

    # Buoc 2: Tim va nhan Daily NFT Check-in
    nft_checkin_btn = find_element_by_selectors(driver, [
        "//p[contains(text(), 'Daily NFT Check-in')]/..",
        "//p[contains(text(), 'Daily NFT Check-in')]/../../..",
        "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div[1]",
    ], wait_time=10)
    if not nft_checkin_btn:
        print(f"[Profile {profile_index}] Khong tim thay Daily NFT Check-in sau 10s")
        return False
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", nft_checkin_btn)
    time.sleep(2)
    try:
        driver.execute_script("arguments[0].click();", nft_checkin_btn)
    except Exception:
        click_element_safe(driver, nft_checkin_btn)
    print(f"[Profile {profile_index}] Da nhan Daily NFT Check-in, cho modal...")
    time.sleep(5)

    # Buoc 3: Modal hien ra → kiem tra button
    modal_btn = find_element_by_selectors(driver, [
        "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div/div/button",
        "/html/body/div/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div/div/button",
        "//button[contains(., 'Check in')]",
        "//button[contains(., 'Mint')]",
    ], wait_time=10)
    if not modal_btn:
        print(f"[Profile {profile_index}] Khong tim thay nut trong modal sau 10s")
        return False

    btn_text = modal_btn.text.strip()
    print(f"[Profile {profile_index}] Thay button modal: '{btn_text}'")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", modal_btn)
    time.sleep(2)

    # ---------- Truong hop 1: Check in ----------
    if "Check in" in btn_text or "Check In" in btn_text:
        click_element_safe(driver, modal_btn)
        print(f"[Profile {profile_index}] Da nhan Check in!")
        time.sleep(15)
        return True

    # ---------- Truong hop 2: Mint ----------
    elif "Mint" in btn_text:
        main_window = driver.current_window_handle
        confirmed = False
        max_mint_retries = 5

        for mint_attempt in range(1, max_mint_retries + 1):
            print(f"[Profile {profile_index}] [Mint attempt {mint_attempt}] Nhan Mint...")

            # Tim lai nut Mint (co the stale sau retry)
            mint_btn = find_element_by_selectors(driver, [
                "/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div/div/button",
                "/html/body/div/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div/div/button",
                "//button[contains(., 'Mint')]",
            ], wait_time=10)
            if not mint_btn:
                print(f"[Profile {profile_index}] [Mint attempt {mint_attempt}] Khong tim thay nut Mint")
                break

            click_element_safe(driver, mint_btn)
            print(f"[Profile {profile_index}] [Mint attempt {mint_attempt}] Da nhan Mint, cho popup MetaMask confirm...")

            # Cho popup confirm xuat hien
            mint_popup = _wait_for_new_window(driver, known_windows={main_window}, timeout=20)
            if not mint_popup:
                print(f"[Profile {profile_index}] [Mint attempt {mint_attempt}] Khong thay popup confirm sau 20s, thu lai...")
                continue

            driver.switch_to.window(mint_popup)
            time.sleep(8)

            # Tim nut Confirm
            confirm_btn = find_element_by_selectors(driver, [
                "//button[contains(., 'Confirm')]",
                "//button[contains(., 'Xac nhan')]",
            ], wait_time=10)

            if confirm_btn:
                click_element_safe(driver, confirm_btn)
                print(f"[Profile {profile_index}] [Mint attempt {mint_attempt}] Da nhan Confirm mint NFT!")
                confirmed = True

                # Tat popup MetaMask
                try:
                    driver.close()
                    print(f"[Profile {profile_index}] Da dong popup MetaMask")
                except Exception:
                    pass
                time.sleep(5)

                # Switch ve main
                if main_window in driver.window_handles:
                    driver.switch_to.window(main_window)
                else:
                    driver.switch_to.window(driver.window_handles[0])
                break

            else:
                print(f"[Profile {profile_index}] [Mint attempt {mint_attempt}] Khong thay Confirm → dong popup, thu lai...")
                try:
                    driver.close()
                except Exception:
                    pass
                time.sleep(2)

                if main_window in driver.window_handles:
                    driver.switch_to.window(main_window)
                else:
                    driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)

        if not confirmed:
            print(f"[Profile {profile_index}] Khong the Confirm sau {max_mint_retries} lan thu")
            return False

        time.sleep(5)

        # Nhan Done trong modal
        done_btn = find_element_by_selectors(driver, [
            "/html/body/div/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div/div/div[5]/button[2]",
            "//button[contains(., 'Done')]",
        ], wait_time=15)
        if done_btn:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", done_btn)
            time.sleep(2)
            click_element_safe(driver, done_btn)
            print(f"[Profile {profile_index}] Da nhan Done!")
        else:
            print(f"[Profile {profile_index}] Khong thay nut Done, bo qua")

        time.sleep(10)
        return True

    else:
        print(f"[Profile {profile_index}] Button khong xac dinh: '{btn_text}', bo qua")
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
    # result = run_fairshare(FIREFOX_PROFILES[0], 1)