import argparse
import os
import subprocess
import sys
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException

url_1 = "https://web.telegram.org/a/#?tgaddr=tg%3A%2F%2Fresolve%3Fdomain%3Donedollar_wallet_bot%26appname%3Ddev"
url_2 = "https://web.telegram.org/a/#?tgaddr=tg%3A%2F%2Fresolve%3Fdomain%3Dpg_super_dev_bot%26appname%3Dtonpass"

DEFAULT_CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEFAULT_USER_DATA_DIR = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
DEFAULT_PROFILE_NAME = "Default"
BUTTON_XPATH = "/html/body/div[4]/div[2]/div/button[1]"
CLICK_COUNT = 6


def build_chrome_options(user_data_dir, profile_name, chrome_path):
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_name}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = chrome_path
    return options


def validate_path(path, description):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{description} does not exist: {path}")


def open_chrome_directly(url, chrome_path, user_data_dir, profile_name):
    command = [
        chrome_path,
        f"--user-data-dir={user_data_dir}",
        f"--profile-directory={profile_name}",
        "--new-window",
        "--start-maximized",
        url,
    ]
    subprocess.Popen(command, shell=False)
    print("Opened Chrome directly with the specified profile.")
    print("If automation could not attach, the script cannot continue clicking automatically.")
    print("Close all Chrome windows using that profile and rerun the script for automation.")


def try_click_in_frames(driver, xpath, depth=0, max_depth=5):
    if depth > max_depth:
        return False
    try:
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", element)
        return True
    except Exception:
        pass

    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for frame in frames:
        try:
            driver.switch_to.frame(frame)
            if try_click_in_frames(driver, xpath, depth + 1, max_depth):
                return True
        except Exception:
            pass
        finally:
            driver.switch_to.parent_frame()

    return False


def wait_and_click(driver, xpath, timeout=30, description=None):
    description = description or xpath
    deadline = time.time() + timeout
    while time.time() < deadline:
        driver.switch_to.default_content()
        if try_click_in_frames(driver, xpath):
            print(f"Clicked: {description}")
            return
        sleep(1)
    raise RuntimeError(f"Could not find or click {description} within {timeout} seconds.")


def click_tma_sequence(driver):
    for i in range(1, CLICK_COUNT + 1):
        wait_and_click(driver, BUTTON_XPATH, timeout=20, description=f"button {i}")
        sleep(1)


def open_TMA(url, chrome_path=DEFAULT_CHROME_PATH, user_data_dir=DEFAULT_USER_DATA_DIR, profile_name=DEFAULT_PROFILE_NAME):
    validate_path(chrome_path, "Chrome executable")
    validate_path(user_data_dir, "Chrome user data directory")

    profile_path = os.path.join(user_data_dir, profile_name)
    if not os.path.isdir(profile_path):
        raise FileNotFoundError(
            f"Chrome profile does not exist in user data dir: {profile_path}."
            " Check the profile-directory name or profile folder."
        )

    options = build_chrome_options(user_data_dir, profile_name, chrome_path)
    try:
        driver = webdriver.Chrome(options=options)
    except (SessionNotCreatedException, WebDriverException) as exc:
        print(f"Chrome failed to start with the profile: {exc}")
        print("This usually happens because the profile is already open in another Chrome instance.")
        print("Automation cannot control the browser in that case.")
        print("Opening the URL in your existing Chrome profile and stopping the script.")
        open_chrome_directly(url, chrome_path, user_data_dir, profile_name)
        return None

    print("Opening Telegram mini app...")
    driver.get(url)
    print("Waiting 30 seconds for the page to load and be ready for clicks...")
    sleep(30)
    click_tma_sequence(driver)

    print("Waiting 15 seconds before clicking the On hold button...")
    sleep(15)
    wait_and_click(driver, "/html/body/main/div/div/div/div[2]/div[3]/div/div/div[1]/div[2]/p", timeout=20, description="On hold button")

    print("Waiting 10 seconds before clicking the Startnew mining section button...")
    sleep(10)
    wait_and_click(driver, "/html/body/main/div/div/div/div[3]/div[1]/div[1]/button", timeout=20, description="Startnew mining section button")

    return driver


def parse_args():
    parser = argparse.ArgumentParser(
        description="Open Telegram mini app on Chrome using a logged-in Chrome profile and click buttons automatically."
    )
    parser.add_argument(
        "--url",
        default=url_1,
        help="Telegram mini app web link, default is url_1.",
    )
    parser.add_argument(
        "--chrome-path",
        default=DEFAULT_CHROME_PATH,
        help="Path to chrome.exe.",
    )
    parser.add_argument(
        "--user-data-dir",
        default=DEFAULT_USER_DATA_DIR,
        help="Chrome User Data directory.",
    )
    parser.add_argument(
        "--profile-name",
        default=DEFAULT_PROFILE_NAME,
        help="Chrome profile name that has Telegram logged in, e.g. Default or Profile 1.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        open_TMA(args.url, args.chrome_path, args.user_data_dir, args.profile_name)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    except RuntimeError as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
