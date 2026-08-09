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
URL = "http://inception.dachain.io/"
METAMASK_PASSWORD = "22091997"
OPEN_BOX_TIMES = 5          # Số lần mở box (OPEN FREE hoặc OPEN FOR 150 QE)

# ==================== SELECTORS ====================

# B1 - Enter Inception & Connect Wallet
ENTER_INCEPTION_SELECTORS = [
    "/html/body/div/div[2]/div[4]/div[3]/button",
    "//button[contains(., 'ENTER INCEPTION')]",
    "//button[contains(., 'Enter Inception')]",
]

WALLET_BUTTON_SELECTORS = [
    "/html/body/div/div[2]/div[7]/div/div/div[2]/button[2]/div[2]/div/span[1]",
    "//button[.//span[contains(text(), 'WALLET')]]",
    "//button[contains(., 'WALLET')]",
    "//button[contains(., 'Wallet')]",
]

# METAMASK_OPTION_SELECTORS không dùng nữa vì modal dùng Shadow DOM (Web Components)
# Thay bằng hàm _click_metamask_in_modal() dùng JavaScript để xuyên shadow root
METAMASK_OPTION_SELECTORS = []  # giữ để không lỗi import

# Đã đăng nhập thành công (có dashboard)
LOGGED_IN_INDICATORS = [
    "//button[contains(., 'Faucet')]",
    "//span[contains(., 'Faucet')]",
    "//*[contains(text(), 'QUANTUM CRATE')]",
    "//*[contains(text(), 'Quantum Crate')]",
    "//*[contains(@class, 'dashboard')]",
]

# B2 - Faucet
FAUCET_MENU_SELECTORS = [
    "//button[contains(., 'Faucet')]",
    "//a[contains(., 'Faucet')]",
    "//span[contains(., 'Faucet')]",
    "//*[contains(text(), 'Faucet')]",
]

FAUCET_CLAIM_SELECTORS = [
    "//button[contains(., 'Claim Testnet')]",
    "/html/body/div/div[2]/div/div/div/div[2]/div[1]/div[2]/button",
]

# B3 - Quantum Crate
QUANTUM_CRATE_SELECTORS = [
    "//*[contains(text(), 'QUANTUM CRATE')]",
    "//*[contains(text(), 'Quantum Crate')]",
    "//button[contains(., 'QUANTUM CRATE')]",
    "//a[contains(., 'QUANTUM CRATE')]",
]

OPEN_FREE_SELECTORS = [
    "//button[contains(., 'OPEN FREE')]",
    "//button[contains(., 'Open Free')]",
    "//button[contains(., 'Open free')]",
]

OPEN_PAID_SELECTORS = [
    "//button[contains(., 'OPEN FOR 150 QE')]",
    "//button[contains(., 'Open for 150')]",
    "//button[contains(., '150 QE')]",
]

CLOSE_SELECTORS = [
    "//button[contains(., 'CLOSE')]",
    "//button[contains(., 'Close')]",
    "//button[@aria-label='close']",
    "//button[@aria-label='Close']",
    "//*[contains(@class, 'close')]//button",
    "//button[contains(@class, 'close')]",
    "//*[@role='dialog']//button[last()]",
    "//button[contains(., '✕')]",
    "//button[contains(., '×')]",
    "//button[contains(., 'X')]",
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
    """Click Connect/Sign/Confirm trong window hiện tại"""
    for selector in [
        "//button[contains(., 'Connect')]",
        "//button[contains(., 'Sign')]",
        "//button[contains(., 'Confirm')]",
    ]:
        btn = find_element_by_selectors(driver, [selector], wait_time=15)
        if btn:
            print(f"[Profile {profile_index}] [{step_label}] Click: {selector}")
            click_element_safe(driver, btn)
            time.sleep(3)
            return True
    print(f"[Profile {profile_index}] [{step_label}] Không thấy button nào để click")
    return False


def _handle_metamask_popup(driver, profile_index, main_window, label="MetaMask"):
    """Xử lý popup MetaMask: unlock nếu cần rồi click Connect/Confirm"""
    popup = _wait_for_new_window(driver, known_windows={main_window}, timeout=15)
    if not popup:
        print(f"[Profile {profile_index}] [{label}] Không thấy popup MetaMask")
        return False

    driver.switch_to.window(popup)
    time.sleep(3)

    # Unlock nếu cần
    pass_el = find_element_by_selectors(driver, ["//input[@type='password']"], wait_time=5)
    if pass_el:
        print(f"[Profile {profile_index}] [{label}] Đang unlock MetaMask...")
        pass_el.send_keys(METAMASK_PASSWORD)
        time.sleep(1)
        unlock_btn = find_element_by_selectors(
            driver,
            ["//button[contains(., 'Unlock')]", "//button[contains(., 'Mở khóa')]"],
            wait_time=15
        )
        if unlock_btn:
            click_element_safe(driver, unlock_btn)
        time.sleep(5)

    _click_metamask_buttons(driver, profile_index, label)

    # Switch về main window
    if main_window in driver.window_handles:
        driver.switch_to.window(main_window)
    else:
        driver.switch_to.window(driver.window_handles[0])
    time.sleep(10)
    return True


def _is_logged_in(driver, profile_index, timeout=30):
    """Kiểm tra đã vào được dashboard chưa"""
    print(f"[Profile {profile_index}] Kiểm tra login thành công...")
    end = time.time() + timeout
    while time.time() < end:
        for indicator in LOGGED_IN_INDICATORS:
            try:
                el = driver.find_element(By.XPATH, indicator)
                if el.is_displayed():
                    print(f"[Profile {profile_index}] Đã vào dashboard!")
                    return True
            except Exception:
                continue
        time.sleep(2)
    print(f"[Profile {profile_index}] Chưa vào được dashboard sau {timeout}s")
    return False


def _scroll_to_element(driver, element):
    """Scroll đến element"""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(1)


def _click_metamask_in_modal(driver, profile_index, timeout=15):
    """
    Click vào MetaMask trong modal Connect Wallet dùng Shadow DOM (Web Components / reown UI).
    Cấu trúc: w3m-modal > shadow > ... > w3m-connect-view > shadow > ... > w3m-list-wallet > shadow > button
    """
    JS_FIND_METAMASK = """
        function getShadowRoot(el) {
            return el && el.shadowRoot ? el.shadowRoot : null;
        }

        function queryDeep(root, selector) {
            if (!root) return null;
            let el = root.querySelector(selector);
            if (el) return el;
            const all = root.querySelectorAll('*');
            for (const node of all) {
                const sr = getShadowRoot(node);
                if (sr) {
                    const found = queryDeep(sr, selector);
                    if (found) return found;
                }
            }
            return null;
        }

        function findMetaMaskButton(root) {
            if (!root) return null;
            // Tìm tất cả w3m-list-wallet trong shadow DOM
            const walletEls = [];
            function collectWallets(r) {
                if (!r) return;
                const items = r.querySelectorAll('w3m-list-wallet');
                items.forEach(i => walletEls.push(i));
                const all = r.querySelectorAll('*');
                for (const node of all) {
                    const sr = getShadowRoot(node);
                    if (sr) collectWallets(sr);
                }
            }
            collectWallets(root);

            for (const wallet of walletEls) {
                const sr = getShadowRoot(wallet);
                if (!sr) continue;
                const btn = sr.querySelector('button');
                if (btn && btn.innerText && btn.innerText.includes('MetaMask')) {
                    return btn;
                }
            }

            // Fallback: tìm button bất kỳ có text MetaMask trong toàn shadow DOM
            function findBtnWithText(r) {
                if (!r) return null;
                const btns = r.querySelectorAll('button');
                for (const btn of btns) {
                    if (btn.innerText && btn.innerText.includes('MetaMask')) return btn;
                }
                const all = r.querySelectorAll('*');
                for (const node of all) {
                    const sr = getShadowRoot(node);
                    if (sr) {
                        const found = findBtnWithText(sr);
                        if (found) return found;
                    }
                }
                return null;
            }
            return findBtnWithText(root);
        }

        const modal = document.querySelector('w3m-modal');
        if (!modal) return null;
        return findMetaMaskButton(modal.shadowRoot || modal);
    """

    end = time.time() + timeout
    while time.time() < end:
        try:
            btn = driver.execute_script(JS_FIND_METAMASK)
            if btn:
                print(f"[Profile {profile_index}] Tìm thấy MetaMask button trong Shadow DOM, đang click...")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", btn)
                return True
        except Exception as e:
            print(f"[Profile {profile_index}] JS Shadow DOM error: {e}")
        time.sleep(2)

    print(f"[Profile {profile_index}] Không tìm thấy MetaMask trong Shadow DOM sau {timeout}s")
    return False


# ==================== BƯỚC 1: Truy cập & Connect Wallet ====================

def step1_access_and_connect(driver, profile_index):
    """B1: Mở trang, nhấn ENTER INCEPTION → WALLET → MetaMask → xử lý popup"""
    print(f"\n[Profile {profile_index}] [B1] Truy cập {URL}...")
    driver.get(URL)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)

    # Kiểm tra nếu đã login sẵn
    if _is_logged_in(driver, profile_index, timeout=5):
        print(f"[Profile {profile_index}] [B1] Đã login sẵn, bỏ qua B1")
        return True

    # --- Nhấn ENTER INCEPTION ---
    enter_btn = find_element_by_selectors(driver, ENTER_INCEPTION_SELECTORS, wait_time=30)
    if not enter_btn:
        print(f"[Profile {profile_index}] [B1] Không tìm thấy nút ENTER INCEPTION")
        return False

    _scroll_to_element(driver, enter_btn)
    click_element_safe(driver, enter_btn)
    print(f"[Profile {profile_index}] [B1] Đã nhấn ENTER INCEPTION")
    time.sleep(5)

    # --- Nhấn WALLET ---
    wallet_btn = find_element_by_selectors(driver, WALLET_BUTTON_SELECTORS, wait_time=15)
    if not wallet_btn:
        print(f"[Profile {profile_index}] [B1] Không tìm thấy nút WALLET")
        return False

    _scroll_to_element(driver, wallet_btn)
    click_element_safe(driver, wallet_btn)
    print(f"[Profile {profile_index}] [B1] Đã nhấn WALLET")
    time.sleep(3)

    # --- Chờ modal Connect Wallet (Shadow DOM / reown UI) hiện ra ---
    print(f"[Profile {profile_index}] [B1] Chờ modal Connect Wallet hiện ra...")
    time.sleep(3)

    # --- Chọn MetaMask trong modal Shadow DOM ---
    main_window = driver.current_window_handle
    if not _click_metamask_in_modal(driver, profile_index, timeout=15):
        print(f"[Profile {profile_index}] [B1] Không tìm thấy MetaMask trong modal")
        return False

    print(f"[Profile {profile_index}] [B1] Đã click MetaMask, chờ popup MetaMask extension...")
    time.sleep(5)

    # --- Xử lý popup MetaMask lần 1 (Connect) ---
    _handle_metamask_popup(driver, profile_index, main_window, label="Connect-Popup1")
    time.sleep(3)

    # --- Có thể có popup thứ 2 (Sign) ---
    popup2 = _wait_for_new_window(driver, known_windows={main_window}, timeout=15)
    if popup2:
        print(f"[Profile {profile_index}] [B1] Thấy popup 2 (Sign), đang xử lý...")
        driver.switch_to.window(popup2)
        time.sleep(3)
        _click_metamask_buttons(driver, profile_index, "Sign-Popup2")
        if main_window in driver.window_handles:
            driver.switch_to.window(main_window)
        else:
            driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)

    # --- Xác nhận đã login ---
    if _is_logged_in(driver, profile_index, timeout=20):
        print(f"[Profile {profile_index}] [B1] Connect thành công!")
        return True

    print(f"[Profile {profile_index}] [B1] Chưa connect được, thử lại lần cuối...")

    # Retry: nhấn lại WALLET rồi chọn MetaMask qua Shadow DOM
    wallet_btn = find_element_by_selectors(driver, WALLET_BUTTON_SELECTORS, wait_time=5)
    if wallet_btn:
        click_element_safe(driver, wallet_btn)
        time.sleep(3)
        main_window = driver.current_window_handle
        if _click_metamask_in_modal(driver, profile_index, timeout=15):
            time.sleep(5)
            _handle_metamask_popup(driver, profile_index, main_window, label="Connect-Retry")
            time.sleep(5)
            popup2 = _wait_for_new_window(driver, known_windows={main_window}, timeout=15)
            if popup2:
                driver.switch_to.window(popup2)
                time.sleep(3)
                _click_metamask_buttons(driver, profile_index, "Sign-Retry")
                if main_window in driver.window_handles:
                    driver.switch_to.window(main_window)
                else:
                    driver.switch_to.window(driver.window_handles[0])
                time.sleep(5)

    return _is_logged_in(driver, profile_index, timeout=30)


# ==================== BƯỚC 2: Faucet ====================

def step2_faucet(driver, profile_index):
    """B2: Nhấn menu Faucet → nhấn button Faucet → đợi 15s"""
    print(f"\n[Profile {profile_index}] [B2] Tìm menu Faucet...")

    faucet_menu = find_element_by_selectors(driver, FAUCET_MENU_SELECTORS, wait_time=15)
    if not faucet_menu:
        print(f"[Profile {profile_index}] [B2] Không tìm thấy menu Faucet")
        return False

    _scroll_to_element(driver, faucet_menu)
    click_element_safe(driver, faucet_menu)
    print(f"[Profile {profile_index}] [B2] Đã nhấn vào Faucet menu")
    time.sleep(3)

    # Tìm button Faucet (có thể là nút Claim Faucet hoặc Faucet chính)
    faucet_claim_selectors_extended = [
        "//*[@id='root']/div[2]/div/div/div/div[2]/div[1]/div[2]/button",
        "//button[contains(., 'Claim Testnet')]",
        "//button[contains(., 'CLAIM TESTNET DACC')]",
    ]

    faucet_btn = find_element_by_selectors(driver, faucet_claim_selectors_extended, wait_time=15)
    if faucet_btn:
        _scroll_to_element(driver, faucet_btn)
        click_element_safe(driver, faucet_btn)
        time.sleep(3)
        click_element_safe(driver, faucet_btn)  # Nhấn lại để đảm bảo
        print(f"[Profile {profile_index}] [B2] Đã nhấn Faucet! Đợi 15 giây...")
    time.sleep(15)

    print(f"[Profile {profile_index}] [B2] Hoàn thành Faucet!")
    return True


# ==================== BƯỚC 3: Quantum Crate ====================

def step3_quantum_crate(driver, profile_index):
    """B3: Tìm QUANTUM CRATE → nhấn vào → sau đó lặp 8 lần: scroll tìm OPEN FREE → nhấn → đợi 15s → đóng"""
    print(f"\n[Profile {profile_index}] [B3] Tìm QUANTUM CRATE...")

    crate_btn = find_element_by_selectors(driver, QUANTUM_CRATE_SELECTORS, wait_time=30)
    if not crate_btn:
        print(f"[Profile {profile_index}] [B3] Không tìm thấy QUANTUM CRATE")
        return False

    _scroll_to_element(driver, crate_btn)
    click_element_safe(driver, crate_btn)
    print(f"[Profile {profile_index}] [B3] Đã nhấn QUANTUM CRATE, bắt đầu vòng lặp mở box...")
    time.sleep(5)

    success_count = 0

    for attempt in range(1, OPEN_BOX_TIMES + 1):
        print(f"\n[Profile {profile_index}] [B3] === Mở box lần {attempt}/{OPEN_BOX_TIMES} ===")

        # --- Scroll tìm OPEN FREE ---
        open_btn = None
        btn_type = "OPEN FREE"

        # Thử tìm ngay trước, nếu không có thì scroll xuống dần
        open_btn = find_element_by_selectors(driver, OPEN_FREE_SELECTORS, wait_time=5)
        if not open_btn:
            print(f"[Profile {profile_index}] [B3] Lần {attempt}: Chưa thấy OPEN FREE, đang scroll tìm...")
            for _ in range(5):
                driver.execute_script("window.scrollBy(0, 200);")
                time.sleep(1)
                open_btn = find_element_by_selectors(driver, OPEN_FREE_SELECTORS, wait_time=3)
                if open_btn:
                    break

        if not open_btn:
            print(f"[Profile {profile_index}] [B3] Lần {attempt}: Không tìm thấy OPEN FREE, bỏ qua lần này")
            continue

        # --- Nhấn OPEN FREE ---
        print(f"[Profile {profile_index}] [B3] Lần {attempt}: Nhấn '{btn_type}'...")
        _scroll_to_element(driver, open_btn)
        click_element_safe(driver, open_btn)

        open_paid_btn = find_element_by_selectors(driver, OPEN_PAID_SELECTORS, wait_time=5)
        if not open_paid_btn:
            break  # Nếu không thấy nút OPEN FOR 150 QE thì coi như đã hết lượt mở free, dừng lại
        if open_paid_btn:
            click_element_safe(driver, open_paid_btn)

        print(f"[Profile {profile_index}] [B3] Lần {attempt}: Đợi 15 giây...")
        time.sleep(15)

        # --- Nhấn CLOSE hoặc X ---
        close_btn = find_element_by_selectors(driver, CLOSE_SELECTORS, wait_time=10)
        if close_btn:
            _scroll_to_element(driver, close_btn)
            click_element_safe(driver, close_btn)
            print(f"[Profile {profile_index}] [B3] Lần {attempt}: Đã đóng popup!")
        else:
            print(f"[Profile {profile_index}] [B3] Lần {attempt}: Không thấy CLOSE/X, thử Escape...")
            try:
                from selenium.webdriver.common.keys import Keys
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            except Exception:
                pass

        time.sleep(3)
        success_count += 1

    print(f"\n[Profile {profile_index}] [B3] Hoàn thành: đã mở {success_count}/{OPEN_BOX_TIMES} box!")
    return success_count > 0


# ==================== MAIN TASK ====================

def run_inception(profile_path, profile_index):
    """Task chính cho mỗi profile"""
    driver = None

    try:
        print(f"\n{'='*60}")
        print(f"[Profile {profile_index}] Bắt đầu Inception DaChain automation...")
        print(f"{'='*60}")

        driver = create_firefox_driver(profile_path)

        # B1: Truy cập & Connect
        if not step1_access_and_connect(driver, profile_index):
            print(f"[Profile {profile_index}] ❌ Thất bại ở B1 (Connect Wallet)")
            return False

        print(f"[Profile {profile_index}] ✅ B1 Hoàn thành!")
        time.sleep(3)

        # B2: Faucet
        # if not step2_faucet(driver, profile_index):
        #     print(f"[Profile {profile_index}] ⚠️ B2 Faucet thất bại (có thể đã claim hôm nay), tiếp tục B3...")
        # else:
        #     print(f"[Profile {profile_index}] ✅ B2 Hoàn thành!")

        # time.sleep(3)

        # B3: Quantum Crate
        if not step3_quantum_crate(driver, profile_index):
            print(f"[Profile {profile_index}] ❌ Thất bại ở B3 (Quantum Crate)")
            return False

        print(f"[Profile {profile_index}] ✅ B3 Hoàn thành!")
        print(f"\n[Profile {profile_index}] 🎉 Inception automation hoàn thành thành công!")
        return True

    except Exception as e:
        print(f"\n[Profile {profile_index}] [ERROR] Lỗi xảy ra: {str(e)}\n")
        return False

    finally:
        if driver:
            try:
                time.sleep(5)
                driver.quit()
            except Exception:
                pass


# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    # Chạy tất cả profiles theo batch
    results = run_all_batches(run_inception, FIREFOX_PROFILES)
    

    # Thống kê kết quả
    total = len(results)
    success = sum(1 for r in results if r)
    print(f"\n{'='*60}")
    print(f"KẾT QUẢ TỔNG KẾT")
    print(f"{'='*60}")
    print(f"Tổng profiles: {total}")
    print(f"Thành công:    {success}")
    print(f"Thất bại:      {total - success}")
    print(f"{'='*60}")