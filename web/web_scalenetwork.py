from web_source import (
    create_firefox_driver,
    find_element_by_selectors,
    click_element_safe,
    FIREFOX_PROFILES,
    run_all_batches,
    scroll_to_element
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    InvalidSessionIdException,
    NoSuchWindowException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
import time
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

#-------------------- CONFIGURATION ====================

Scale_Network_URL = "https://mine.sible.network/login"
#--------------------------------------------------------

def access_scale_network(driver, profile_index):
    """Step N1: Access Scale Network login page"""
    try:
        print(f"[Profile {profile_index}] [N1] Accessing {Scale_Network_URL}...")
        driver.get(Scale_Network_URL)

        # Wait for page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)

        print(f"[Profile {profile_index}] [N1] Page loaded successfully")
        return True

    except Exception as e:
        print(
            f"[Profile {profile_index}] [N1] Error accessing page "
            f"({type(e).__name__}): {e!r}"
        )
        return False


def login_and_checkin_scale_network(driver, profile_index):
    main_window = driver.current_window_handle
    time.sleep(2)
    close_selectors = [
        "/html/body/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/div/div/div/div/button",
        "button.css-g5y9jx:nth-child(2)",
        
    ]
    button_close = find_element_by_selectors(driver, close_selectors, 5)
    if button_close:
        scroll_to_element(driver, button_close)
        click_element_safe(driver, button_close)
        time.sleep(2)

    dashboard_selector = "[data-testid='session-card']"

    def dashboard_is_ready(current_driver):
        try:
            current_driver.switch_to.window(main_window)
            return bool(
                current_driver.find_elements(By.CSS_SELECTOR, dashboard_selector)
            )
        except NoSuchWindowException:
            return False

    if dashboard_is_ready(driver):
        print(f"[Profile {profile_index}] Already logged in to Scale Network")
    else:
        google_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div[id$='-overlay'][role='button'], "
                    "div[aria-label*='Google'][role='button']",
                )
            )
        )
        scroll_to_element(driver, google_button)
        try:
            ActionChains(driver).move_to_element(google_button).click().perform()
        except WebDriverException as error:
            print(
                f"[Profile {profile_index}] Could not click Google button: "
                f"{error}"
            )
            return False

        def find_google_window(current_driver):
            for window in current_driver.window_handles:
                try:
                    current_driver.switch_to.window(window)
                    if "accounts.google.com" in current_driver.current_url:
                        return window
                except NoSuchWindowException:
                    continue
            return False

        print(f"[Profile {profile_index}] Waiting for Google OAuth...")
        try:
            google_window = WebDriverWait(driver, 30).until(
                find_google_window
            )
        except TimeoutException:
            print(
                f"[Profile {profile_index}] Google OAuth page did not open; "
                f"windows={len(driver.window_handles)}"
            )
            return False

        driver.switch_to.window(google_window)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        account_selector = (
            "//div[@role='link' and @data-identifier] | "
            "//li[1]//div[@role='link']"
        )
        google_accounts = driver.find_elements(By.XPATH, account_selector)
        if google_accounts:
            scroll_to_element(driver, google_accounts[0])
            try:
                ActionChains(driver).move_to_element(
                    google_accounts[0]
                ).click().perform()
            except (NoSuchWindowException, StaleElementReferenceException):
                pass

            def account_selection_finished(current_driver):
                if google_window not in current_driver.window_handles:
                    return True
                try:
                    current_driver.switch_to.window(google_window)
                    path = current_driver.current_url.split("?", 1)[0].rstrip("/")
                    return not path.endswith("/v3/signin/accountchooser")
                except NoSuchWindowException:
                    return True

            try:
                WebDriverWait(driver, 30).until(account_selection_finished)
            except TimeoutException:
                print(
                    f"[Profile {profile_index}] Google account selection "
                    "did not advance"
                )
                return False

        if google_window in driver.window_handles:
            try:
                driver.switch_to.window(google_window)
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                oauth_url = driver.current_url
            except NoSuchWindowException:
                oauth_url = ""

            if "accounts.google.com" in oauth_url:
                oauth_body = driver.find_element(By.TAG_NAME, "body").text
                oauth_path = oauth_url.split("?", 1)[0]
                if "/signin/oauth/" in oauth_path and "sible.network" in oauth_body:
                    consent_xpath = (
                        "//button[contains(translate(normalize-space(.), "
                        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                        "'continue') or "
                        "contains(translate(normalize-space(.), "
                        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                        "'tiếp tục') or "
                        "contains(translate(normalize-space(.), "
                        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                        "'allow') or "
                        "contains(translate(normalize-space(.), "
                        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
                        "'cho phép')]"
                    )
                    try:
                        consent_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, consent_xpath))
                        )
                    except TimeoutException:
                        print(
                            f"[Profile {profile_index}] Google consent page "
                            "has no Continue/Allow button"
                        )
                        return False
                    ActionChains(driver).move_to_element(
                        consent_button
                    ).click().perform()
                elif "/v3/signin/accountchooser" in oauth_path:
                    print(
                        f"[Profile {profile_index}] Google is still asking "
                        "for an account selection"
                    )
                    return False

        try:
            WebDriverWait(driver, 60).until(dashboard_is_ready)
        except TimeoutException:
            try:
                driver.switch_to.window(main_window)
                print(
                    f"[Profile {profile_index}] Google login did not return "
                    f"to the dashboard (URL: {driver.current_url})"
                )
            except NoSuchWindowException:
                print(f"[Profile {profile_index}] Main browser window was closed")
            return False
        print(f"[Profile {profile_index}] Google login completed")

    time.sleep(8)

    try:
        mine_orb = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button[data-testid='mine-orb'][aria-label='Sible AI']",
                )
            )
        )
    except TimeoutException:
        mine_orb = None

    if mine_orb:
        scroll_to_element(driver, mine_orb)
        if not click_element_safe(driver, mine_orb):
            print(f"[Profile {profile_index}] Could not click Sible AI")
            return False
        print(f"[Profile {profile_index}] Clicked Sible AI; waiting 8 seconds")
        time.sleep(8)
    else:
        print(
            f"[Profile {profile_index}] Sible AI button not found; "
            "continuing because it may already be open"
        )

    try:
        go_back_button = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@aria-label='Go back' or "
                    "normalize-space(.)='Go back']",
                )
            )
        )
    except TimeoutException:
        print(
            f"[Profile {profile_index}] Go back button did not appear after "
            "Sible AI; continuing with the current dashboard"
        )
    else:
        scroll_to_element(driver, go_back_button)
        if not click_element_safe(driver, go_back_button):
            print(f"[Profile {profile_index}] Could not click Go back")
            return False
        print(f"[Profile {profile_index}] Clicked Go back")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, dashboard_selector)
            )
        )

    def click_action(labels, action_name, wait_time=8, fallback_selectors=None):
        text_condition = " or ".join(
            f"contains(normalize-space(.), '{label}')"
            for label in labels
        )
        selector = (
            f"//*[self::button or @role='button'][{text_condition}] | "
            f"//*[({text_condition})]/ancestor::*"
            "[self::button or @role='button'][1] | "
            f"//*[self::button or @role='button'][@aria-label='{labels[0]}']"
        )
        element = find_element_by_selectors(driver, [selector], wait_time)
        if not element:
            if fallback_selectors:
                element = find_element_by_selectors(
                    driver, fallback_selectors, 3
                )
            if element:
                print(f"[Profile {profile_index}] Found {action_name} by DOM structure")
            else:
                print(f"[Profile {profile_index}] {action_name} button not found")
                return False
        try:
            scroll_to_element(driver, element)
            if not click_element_safe(driver, element):
                raise WebDriverException(f"all click methods failed for {action_name}")
            return True
        except StaleElementReferenceException:
            print(f"[Profile {profile_index}] {action_name} button became stale")
            return False
        except InvalidSessionIdException:
            print(f"[Profile {profile_index}] Browser session ended during {action_name}")
            return False
        except WebDriverException as error:
            print(f"[Profile {profile_index}] Could not click {action_name}: {error}")
            return False

    active_mining_selectors = [
        "//button[@aria-label='Start mining']",
        "//*[@role='button' and @aria-label='Start mining']",
        "//button[contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
        "'start mining')]",
        "//*[@role='button' and contains(translate(normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
        "'start mining')]",
        "//button[contains(normalize-space(.), 'Kích hoạt phiên đào')]",
        "//*[@role='button' and contains(normalize-space(.), 'Kích hoạt phiên đào')]",
        "//*[@role='button' and contains(normalize-space(.), 'Activate mining session')]",
        "//*[self::button or @role='button'][contains("
        "translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'), 'start mining')]",
        "//*[self::button or @role='button'][contains("
        "normalize-space(@aria-label), 'Kích hoạt đào')]",
        "//*[contains(normalize-space(.), 'Kích hoạt đào để tăng tốc')]"
        "/ancestor::*[self::button or @role='button'][1]",
        # Legacy icon-only fallback for versions that expose no text or
        # aria-label on the mining control.
        "//button[@type='button' and contains(@style, 'width: 60px') "
        "and .//*[local-name()='svg']]",
    ]
    try:
        active_mining_button = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located(
                (By.XPATH, " | ".join(active_mining_selectors))
            )
        )
    except TimeoutException:
        active_mining_button = None

    if active_mining_button:
        print(f"[Profile {profile_index}] Found Start Mining button")
        try:
            active_mining_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(active_mining_button)
            )
            scroll_to_element(driver, active_mining_button)
            if not click_element_safe(driver, active_mining_button):
                raise WebDriverException("all click methods failed")
        except StaleElementReferenceException:
            print(f"[Profile {profile_index}] Start Mining button became stale")
            return False
        except (InvalidSessionIdException, WebDriverException) as error:
            print(f"[Profile {profile_index}] Could not click Start Mining: {error}")
            return False
    else:
        ai_accelerate = driver.find_elements(
            By.CSS_SELECTOR, "[data-testid='ai-accelerate']"
        )
        if ai_accelerate:
            accelerate_buttons = ai_accelerate[0].find_elements(
                By.CSS_SELECTOR, "button[aria-label='Accelerate']"
            )
            disabled_count = sum(
                not button.is_enabled() for button in accelerate_buttons
            )
            print(
                f"[Profile {profile_index}] Dashboard loaded, but the current "
                "UI has no Start Mining control; "
                f"{disabled_count}/{len(accelerate_buttons)} AI Accelerate "
                "buttons are disabled"
            )
        else:
            print(
                f"[Profile {profile_index}] Start Mining button not found; "
                "continuing because mining may already be active"
            )

    if click_action(["Claim", "Nhận thưởng"], "Claim"):
        time.sleep(2)

    if click_action(["Okay", "Đồng ý", "Đồng Ý"], "Okay"):
        time.sleep(2)

    for cycle, wait_after_confirmation in enumerate((36, 36, 12), start=1):
        print(f"[Profile {profile_index}] Acceleration cycle {cycle}/3")
        if click_action(
            ["Accelerate", "Tăng tốc"],
            "Accelerate",
            3,
            [
                "//*[@id='root']/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div[4]/button/div",
            ],
        ):
            time.sleep(2)
        if click_action(
            ["Got it", "Đã hiểu"],
            "Got it",
            3,
            [
                "//*[@id='root']/div/div/div[1]/div[3]/div/div/div[2]/div/button/div",
            ],
        ):
            time.sleep(wait_after_confirmation)

    return True

def run_scale_network_script(profile_path, profile_index):
    """Chạy automation script cho Scale Network"""
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"\n[Profile {profile_index}] Starting Scale Network automation...")
        print(f"{'='*60}")
        driver = create_firefox_driver(profile_path)
        
        if not access_scale_network(driver, profile_index):
            return False
        
        if not login_and_checkin_scale_network(driver, profile_index):
            return False
        
        
        print(f"[Profile {profile_index}] Scale Network automation completed successfully")
        return True

    except Exception as e:
        print(f"[Profile {profile_index}] Error ({type(e).__name__}): {e!r}")
        return False

    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


if __name__ == "__main__":

    # run_scale_network_script(FIREFOX_PROFILES[0], 1)  # Chạy thử cho profile đầu tiên
    results = run_all_batches(run_scale_network_script, FIREFOX_PROFILES)
    total = len(results)
    success = sum(1 for r in results if r)
    print(f"\n{'='*60}")
    print(f"KẾT QUẢ TỔNG KẾT")
    print(f"{'='*60}")
    print(f"Tổng profiles: {total}")
    print(f"Thành công:    {success}")
    print(f"Thất bại:      {total - success}")
    print(f"{'='*60}")
    