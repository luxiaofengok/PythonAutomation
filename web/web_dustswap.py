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
URL = "https://app.dustswap.wtf/?ref=DUST-I7DK1"
METAMASK_PASSWORD = "22091997"

CONNECT_WALLET_SELECTORS = [
    "//button[contains(., 'Connect Wallet')]",
    "//button[contains(., 'Kết nối ví')]",
]

# ==================== ACCESS ====================
def access_dustswap(driver, profile_index):

    try:
        print(f"[Profile {profile_index}] [N1] Accessing {URL}...")
        driver.get(URL)

        # Wait for page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)

        print(f"[Profile {profile_index}] [N1] Page loaded successfully")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] [N1] Error accessing page: {str(e)}")
        return False


def _scroll_to_element(driver, element):
    """Scroll đến element"""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(1)


def _safe_current_window(driver):
    """
    Lấy window handle hiện tại một cách an toàn.
    Trả về None nếu window đã bị đóng/discard (ví dụ MetaMask tự đóng popup
    sau khi Confirm), thay vì để driver.current_window_handle ném NoSuchWindowError.
    """
    try:
        return driver.current_window_handle
    except Exception:
        return None


def _safe_switch_window(driver, handle, profile_index, fallback_handle=None):
    """
    Switch sang 1 window một cách an toàn.
    Nếu handle đó đã đóng, thử fallback_handle (thường là main_window).
    Trả về True nếu switch thành công, False nếu cả 2 đều thất bại.
    """
    for h in [handle, fallback_handle]:
        if h is None:
            continue
        try:
            driver.switch_to.window(h)
            return True
        except Exception:
            continue
    print(f"[Profile {profile_index}] LỖI: không switch được sang bất kỳ window nào (cả handle chính và fallback đều đã đóng)")
    return False


def _click_metamask_buttons(driver, profile_index):
    """
    Click Connect/Sign/Confirm trong window hiện tại, trả về True nếu click được.
    Dùng find_element_by_selectors gốc (đã sửa, không còn bị crash vì LavaMoat
    của MetaMask) — dùng thống nhất cho cả MetaMask và trang web.
    """
    time.sleep(5)
    for selector in [
        "//button[contains(., 'Connect')]",
        "//button[contains(., 'Sign')]",
        "//button[contains(., 'Confirm')]",
        "//button[contains(., 'Next')]",
        "//button[contains(., 'Approve')]",
    ]:
        btn = find_element_by_selectors(driver, [selector], wait_time=8)
        if btn:
            print(f"[Profile {profile_index}] Click: {selector}")
            click_element_safe(driver, btn)
            time.sleep(8)
            return True
    print(f"[Profile {profile_index}] Không thấy button nào để click (url hiện tại: {driver.current_url})")
    return False


def _handle_popup1(driver, profile_index, main_window=None):
    """
    Xử lý popup MetaMask: nhập password + unlock (nếu cần), rồi click Connect/Sign/Confirm.

    Sau khi Unlock, MetaMask có thể:
    (a) chuyển route trong CÙNG window (URL hash đổi từ #/unlock sang #/connect...), hoặc
    (b) đóng popup cũ và mở popup mới.
    Hàm này theo dõi cả 2 trường hợp bằng cách so sánh URL + số lượng window trước/sau.

    Trả về True nếu xử lý được ít nhất 1 trong 2 bước (unlock hoặc click button).
    """
    print(f"[Profile {profile_index}] _handle_popup1: current title='{driver.title}', url='{driver.current_url}'")

    did_something = False

    pass_el = find_element_by_selectors(driver, [
        "//input[@data-testid='unlock-password']",
        "//input[@id='password']",
        "//input[@type='password']",
    ], wait_time=8)

    if pass_el:
        print(f"[Profile {profile_index}] Tìm thấy input password, đang nhập...")
        try:
            pass_el.click()
        except Exception:
            pass
        try:
            pass_el.clear()
        except Exception:
            pass
        pass_el.send_keys(METAMASK_PASSWORD)
        time.sleep(1)

        unlock_btn = find_element_by_selectors(driver, [
            "//button[@data-testid='unlock-submit']",
            "//button[contains(., 'Unlock')]",
            "//button[contains(., 'Mở khóa')]",
        ], wait_time=8)

        if unlock_btn:
            print(f"[Profile {profile_index}] Click Unlock")
            url_before = driver.current_url
            handles_before = set(driver.window_handles)
            unlock_window = driver.current_window_handle

            click_element_safe(driver, unlock_btn)
            did_something = True

            # Chờ và phát hiện thay đổi: route đổi (URL hash khác) HOẶC window thay đổi
            route_changed = False
            end_time = time.time() + 30
            while time.time() < end_time:
                time.sleep(2)
                handles_now = set(driver.window_handles)

                if unlock_window not in handles_now:
                    # window unlock đã đóng -> switch sang window còn lại (không phải main_window)
                    remaining = [h for h in handles_now if main_window is None or h != main_window]
                    if remaining:
                        driver.switch_to.window(remaining[0])
                        print(f"[Profile {profile_index}] [post-unlock] Window unlock đã đóng, switch sang url='{driver.current_url}'")
                    route_changed = True
                    break

                if handles_now != handles_before:
                    # có window mới xuất hiện (mà window cũ vẫn còn) -> switch sang window mới
                    new_handles = handles_now - handles_before
                    driver.switch_to.window(next(iter(new_handles)))
                    print(f"[Profile {profile_index}] [post-unlock] Window mới xuất hiện, switch sang url='{driver.current_url}'")
                    route_changed = True
                    break

                # vẫn cùng window, check xem URL (hash route) đã đổi chưa
                try:
                    url_now = driver.current_url
                except Exception:
                    url_now = url_before
                if url_now != url_before:
                    print(f"[Profile {profile_index}] [post-unlock] Route đổi trong cùng window: '{url_before}' -> '{url_now}'")
                    route_changed = True
                    break

            if not route_changed:
                print(f"[Profile {profile_index}] [post-unlock] Không thấy route/window đổi sau 30s, url hiện tại: '{driver.current_url}'")
        else:
            print(f"[Profile {profile_index}] CẢNH BÁO: Có input password nhưng không thấy nút Unlock")
        time.sleep(2)
    else:
        print(f"[Profile {profile_index}] Không thấy input password (có thể MetaMask đã unlock từ trước)")

    clicked = _click_metamask_buttons(driver, profile_index)
    did_something = did_something or clicked

    if not did_something:
        print(f"[Profile {profile_index}] LỖI: _handle_popup1 không làm được gì cả — có thể đang ở sai window")

    return did_something


def handle_popups(driver, profile_index):
    metamask_btn = find_element_by_selectors(driver, ["//button[contains(., 'MetaMask')]"], wait_time=10)
    if not metamask_btn:
        print(f"[Profile {profile_index}] [B2] Khong thay MetaMask button sau 10s, skip B2")
        return False
    click_element_safe(driver, metamask_btn)
    time.sleep(5)
    return True


def _switch_to_metamask_window(driver, main_window, profile_index, timeout=30):
    """
    Tìm và switch sang window MetaMask (extension popup).
    Trả về True nếu switch thành công, False nếu hết timeout không tìm thấy.
    """
    end_time = time.time() + timeout
    attempt = 0
    while time.time() < end_time:
        attempt += 1
        handles = driver.window_handles
        print(f"[Profile {profile_index}] [switch attempt {attempt}] window_handles: {len(handles)}")

        for handle in handles:
            if handle == main_window:
                continue
            driver.switch_to.window(handle)
            try:
                url = driver.current_url
                title = driver.title
            except Exception:
                continue
            print(f"[Profile {profile_index}]   -> handle={handle[:8]} title='{title}' url='{url[:60]}'")
            if "moz-extension" in url or "extension" in url or "MetaMask" in title:
                print(f"[Profile {profile_index}] Switch thành công sang MetaMask window")
                return True
        time.sleep(2)

    print(f"[Profile {profile_index}] LỖI: Không tìm thấy MetaMask window sau {timeout}s")
    # Quay lại main window để code phía sau không bị treo ở window lạ
    try:
        driver.switch_to.window(main_window)
    except Exception:
        pass
    return False


def _is_already_checked_in(driver, profile_index):
    """
    Kiểm tra xem nút check-in đã ở trạng thái 'Checked In Today' / disable chưa.
    Trả về True nếu đã check-in rồi (nên bỏ qua bước click check-in).
    """
    already_checked_selectors = [
        "//span[contains(., 'Checked In Today')]",
        "//span[contains(., 'Already checked')]",
        "/html/body/div[1]/main/div/div/section[2]/div[2]/div[4]/button/span[2]",
    ]
    for selector in already_checked_selectors:
        try:
            els = driver.find_elements(By.XPATH, selector)
            for el in els:
                try:
                    text = (el.text or "").strip().lower()
                except Exception:
                    text = ""
                if "checked in today" in text or "already checked" in text:
                    print(f"[Profile {profile_index}] Phát hiện đã check-in rồi (text='{text}'), bỏ qua bước check-in")
                    return True
        except Exception as e:
            print(f"[Profile {profile_index}] Lỗi khi check trạng thái check-in với selector '{selector}': {e}")
            continue

    # Kiểm tra thêm: nếu nút check-in có attribute disabled
    try:
        check_in_btns = driver.find_elements(
            By.XPATH,
            "/html/body/div[1]/main/div/div/section[2]/div[2]/div[4]/button"
        )
        for btn in check_in_btns:
            disabled_attr = btn.get_attribute("disabled")
            if disabled_attr is not None:
                print(f"[Profile {profile_index}] Nút check-in có attribute disabled, bỏ qua bước check-in")
                return True
    except Exception as e:
        print(f"[Profile {profile_index}] Lỗi khi check attribute disabled: {e}")

    return False


def connect_and_checkin(driver, profile_index):
    main_window = driver.current_window_handle
    connect_selectors = [
        "/html/body/div/main/div/div[2]/div/section/div[2]/div/button/span[2]",
        "//span[contains(., 'Connect wallet')]",
    ]
    connect_wallet_button = find_element_by_selectors(driver, connect_selectors, 5)
    if connect_wallet_button:
        _scroll_to_element(driver, connect_wallet_button)
        click_element_safe(driver, connect_wallet_button)
        time.sleep(2)
        popup_ok = handle_popups(driver, profile_index)
        if not popup_ok:
            print(f"[Profile {profile_index}] CẢNH BÁO: không click được nút MetaMask trên trang web")
    else:
        print(f"[Profile {profile_index}] LỖI: Không tìm thấy nút 'Connect wallet' trên trang")
        return False

    time.sleep(10)

    switched = _switch_to_metamask_window(driver, main_window, profile_index)
    if not switched:
        print(f"[Profile {profile_index}] LỖI: Dừng lại vì không vào được MetaMask window để unlock")
        return False

    time.sleep(5)
    handled = _handle_popup1(driver, profile_index, main_window=main_window)
    if not handled:
        print(f"[Profile {profile_index}] CẢNH BÁO: _handle_popup1 không xử lý được gì, vẫn tiếp tục thử...")

    # Quay lại main window trước khi tương tác tiếp với trang web
    try:
        driver.switch_to.window(main_window)
    except Exception as e:
        print(f"[Profile {profile_index}] LỖI: main_window đã bị đóng hoặc không truy cập được: {e}")
        return False
    time.sleep(30)

    # add_referral_selectors = [
    #     "/html/body/div/main/div/div/div/section/div[2]/div[4]/button[2]",
    #     "//button[contains(., 'Add referral')]",
    # ]
    # add_referral_button = find_element_by_selectors(driver, add_referral_selectors, 5)
    # if add_referral_button:
    #     _scroll_to_element(driver, add_referral_button)
    #     click_element_safe(driver, add_referral_button)
    #     time.sleep(2)

    main_window = driver.current_window_handle

    # ==== KIỂM TRA ĐÃ CHECK-IN HAY CHƯA TRƯỚC KHI CLICK ====
    if _is_already_checked_in(driver, profile_index):
        print(f"[Profile {profile_index}] Đã check-in hôm nay rồi, bỏ qua bước check-in, đi thẳng tới Spin")
    else:
        reset_selectors = [
            "/html/body/div/main/div/div/section[3]/div[2]/div[4]/button[2]",
            "//button[contains(., 'Reset Streak to 0')]",
        ]
        reset_button = find_element_by_selectors(driver, reset_selectors, 15)
        if reset_button:
            _scroll_to_element(driver, reset_button)
            click_element_safe(driver, reset_button)
            time.sleep(10)

        check_in_selectors = [
            "/html/body/div/main/div/div/section[4]/div[2]/div[4]/button/span[2]",
            "//span[contains(., 'Check in')]",
        ]
        check_in_button = find_element_by_selectors(driver, check_in_selectors, 15)
        if check_in_button:
            _scroll_to_element(driver, check_in_button)
            click_element_safe(driver, check_in_button)

        switched = _switch_to_metamask_window(driver, main_window, profile_index, timeout=15)
        if not switched and check_in_button:
            _scroll_to_element(driver, check_in_button)
            click_element_safe(driver, check_in_button)
            switched = _switch_to_metamask_window(driver, main_window, profile_index, timeout=15)

        if switched:
            time.sleep(10)
            _click_metamask_buttons(driver, profile_index)
            time.sleep(8)
            metamask_window = _safe_current_window(driver)
            if metamask_window is None:
                # Window đã tự đóng (thường xảy ra sau khi click Confirm) -> không cần close nữa
                print(f"[Profile {profile_index}] MetaMask popup đã tự đóng sau khi Confirm, không cần driver.close()")
            elif metamask_window != main_window:
                try:
                    driver.close()
                except Exception:
                    pass
            else:
                print(f"[Profile {profile_index}] CẢNH BÁO: tránh đóng main_window (đang ở cùng window với main)")

        if not _safe_switch_window(driver, main_window, profile_index):
            return False
        time.sleep(30)

    spin_selectors = [
        "/html/body/div/nav[1]/div[2]/a[2]",
        "//a[contains(., 'Spin')]",
    ]
    spin_button = find_element_by_selectors(driver, spin_selectors, 5)
    if spin_button:
        _scroll_to_element(driver, spin_button)
        click_element_safe(driver, spin_button)

    time.sleep(10)

    for i in range(4):
        main_window = _safe_current_window(driver)
        if main_window is None:
            print(f"[Profile {profile_index}] LỖI: không lấy được main_window ở đầu vòng spin {i+1}, dừng lại")
            return False
        spin_wheel_selectors = [
            "/html/body/div/main/div/div/section[2]/div/div[2]/button",
            "//button[contains(., 'Spin')]",
        ]
        spin_wheel_button = find_element_by_selectors(driver, spin_wheel_selectors, 10)
        if not spin_wheel_button:
            return False
        _scroll_to_element(driver, spin_wheel_button)
        click_element_safe(driver, spin_wheel_button)

        time.sleep(10)

        switched = _switch_to_metamask_window(driver, main_window, profile_index, timeout=15)
        if switched:
            time.sleep(10)
            _click_metamask_buttons(driver, profile_index)
            time.sleep(10)
            metamask_window = _safe_current_window(driver)
            if metamask_window is None:
                print(f"[Profile {profile_index}] MetaMask popup đã tự đóng sau khi Confirm, không cần driver.close()")
            elif metamask_window != main_window:
                try:
                    driver.close()
                except Exception:
                    pass
            else:
                print(f"[Profile {profile_index}] CẢNH BÁO: tránh đóng main_window (đang ở cùng window với main)")

        if not _safe_switch_window(driver, main_window, profile_index):
            return False
        time.sleep(15)

    return True


def run_dustswap_script(profile_path, profile_index):
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"\n[Profile {profile_index}] Starting DUSTSWAP automation...")
        print(f"{'='*60}")
        driver = create_firefox_driver(profile_path)

        if not access_dustswap(driver, profile_index):
            return False

        if not connect_and_checkin(driver, profile_index):
            return False

        print(f"[Profile {profile_index}] DUSTSWAP automation completed successfully")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] Error: {str(e)}")
        return False

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

if __name__ == "__main__":

    results = run_all_batches(run_dustswap_script, FIREFOX_PROFILES)
    total = len(results)
    success = sum(1 for r in results if r)
    print(f"\n{'='*60}")
    print(f"KẾT QUẢ TỔNG KẾT")
    print(f"{'='*60}")
    print(f"Tổng profiles: {total}")
    print(f"Thành công:    {success}")
    print(f"Thất bại:      {total - success}")
    print(f"{'='*60}")