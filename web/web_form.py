from web_source import (
    create_firefox_driver,
    check_and_login,
    login_with_google,
    find_element_by_selectors,
    click_element_safe,
    FIREFOX_PROFILES,
    run_all_batches,
    scroll_to_element
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#==================== CONFIGURATION ====================
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeIze7LtTmA7FZ4cJ5WzRs7kE85INi10pIGzvY7zzzJo5rTKA/viewform?pli=1"
DISCORD_IDS_FILE = r"C:\Users\Admin\Downloads\iddiscord.txt"
DISCORD_USERNAMES_FILE = r"C:\Users\Admin\Downloads\mydiscord.txt"
FORM_ACTION_DELAY = 1
AFTER_SUBMIT_DELAY = 5

#========================================================

def access_form(driver, profile_index):
    """Step N1: Access the Google Form"""
    try:
        print(f"[Profile {profile_index}] [N1] Accessing {FORM_URL}...")
        driver.get(FORM_URL)

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


def fill_form(driver, profile_index):
    """Fill and submit the form for one Firefox profile."""
    try:
        discord_id, discord_username = _profile_values(profile_index)
        form = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//form"))
        )

        _fill_question_input(form, "What's your Discord ID?", discord_id)
        time.sleep(FORM_ACTION_DELAY)
        _fill_question_input(form, "What's your Discord Username?", discord_username)
        time.sleep(FORM_ACTION_DELAY)

        email_checkbox = WebDriverWait(form, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//*[@role='checkbox']"))
        )
        if email_checkbox.get_attribute("aria-checked") != "true":
            scroll_to_element(driver, email_checkbox)
            if not click_element_safe(driver, email_checkbox):
                raise RuntimeError("Could not select the email recording checkbox")
            time.sleep(FORM_ACTION_DELAY)

        answers = (
            ("Which responsibilities belong to Supervisory Nodes?",
             "Epoch sealing, checkpoint creation, and randomness accumulation"),
            ("Why are DAC’s D-Wave Advantage processors distributed across multiple locations?",
             "To reduce single-point-of-failure risks"),
            ("Why is MEV extraction limited for validators outside the designated validator set before entropy revelation?",
              "Pending transaction content is hidden from them"),
            ("Which two mechanisms provide replay protection in DAC?",
             "The EVM account nonce and the spent flag for the entropy index"),
            ("How many D-Wave Advantage processors does DAC operate for PoQW mining?", "4"),
        )
        for question, answer in answers:
            _select_radio_answer(form, question, answer, driver)
            time.sleep(FORM_ACTION_DELAY)

        submit = WebDriverWait(form, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    ".//div[@role='button' and "
                    "(@aria-label='Submit' or normalize-space()='Submit' or "
                    "normalize-space()='Gửi')]",
                )
            )
        )
        scroll_to_element(driver, submit)
        if not click_element_safe(driver, submit):
            raise RuntimeError("Could not submit the form")
        print(f"[Profile {profile_index}] [N2] Form submitted successfully")
        time.sleep(AFTER_SUBMIT_DELAY)
        return True
    except Exception as exc:
        print(f"[Profile {profile_index}] [N2] Form error: {exc}")
        return False


def _profile_values(profile_index):
    if not 1 <= profile_index <= len(FIREFOX_PROFILES):
        raise ValueError(f"Invalid profile index: {profile_index}")

    def read_values(path):
        with open(path, "r", encoding="utf-8") as data_file:
            return [line.strip() for line in data_file if line.strip()]

    discord_ids = read_values(DISCORD_IDS_FILE)
    usernames = read_values(DISCORD_USERNAMES_FILE)
    expected = len(FIREFOX_PROFILES)
    if len(discord_ids) != expected or len(usernames) != expected:
        raise ValueError(
            f"Expected {expected} IDs and usernames, got "
            f"{len(discord_ids)} IDs and {len(usernames)} usernames"
        )
    position = profile_index - 1
    return discord_ids[position], usernames[position]


def _question_container(form, question):
    return WebDriverWait(form, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, ".//div[@role='listitem'][.//*[normalize-space()="
             f"{_xpath_literal(question)}]]")
        )
    )


def _fill_question_input(form, question, value):
    container = _question_container(form, question)
    field = WebDriverWait(container, 10).until(
        EC.element_to_be_clickable((By.XPATH, ".//input[@type='text']"))
    )
    field.clear()
    field.send_keys(value)
    time.sleep(FORM_ACTION_DELAY)


def _select_radio_answer(form, question, answer, driver):
    container = _question_container(form, question)
    option = WebDriverWait(container, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, ".//*[@role='radio' and @aria-label="
             f"{_xpath_literal(answer)}]")
        )
    )
    if option.get_attribute("aria-checked") != "true":
        scroll_to_element(driver, option)
        if not click_element_safe(driver, option):
            raise RuntimeError(f"Could not select answer: {answer}")
        time.sleep(FORM_ACTION_DELAY)


def _xpath_literal(value):
    if "'" not in value:
        return f"'{value}'"
    if '"' not in value:
        return f'"{value}"'
    parts = value.split("'")
    return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"


def run_form_script(profile_path, profile_index):
    driver = None
    try:
        print(f"\n[Profile {profile_index}] Starting form automation")
        driver = create_firefox_driver(profile_path)
        if not access_form(driver, profile_index):
            return False
        return fill_form(driver, profile_index)
    except Exception as exc:
        print(f"[Profile {profile_index}] Unexpected error: {exc}")
        return False
    finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass


if __name__ == "__main__":
    # run_form_script(FIREFOX_PROFILES[20], 21)  # Test with the first profile
     
    results = run_all_batches(run_form_script, FIREFOX_PROFILES)
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
