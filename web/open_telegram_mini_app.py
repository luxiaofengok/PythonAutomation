import argparse
import os
import subprocess
import sys

DEFAULT_CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEFAULT_USER_DATA_DIR = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
DEFAULT_PROFILE_NAME = "Default"
DEFAULT_URL = "https://web.telegram.org/a/#?tgaddr=tg%3A%2F%2Fresolve%3Fdomain%3Donedollar_wallet_bot%26appname%3Ddev"


def build_chrome_command(url, chrome_path, user_data_dir, profile_name):
    command = [chrome_path]
    command.append(f"--user-data-dir={user_data_dir}")
    command.append(f"--profile-directory={profile_name}")
    command.append("--new-window")
    command.append(url)
    return command


def validate_path(path, description):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{description} không tồn tại: {path}")


def open_telegram_mini_app(url, chrome_path, user_data_dir, profile_name):
    validate_path(chrome_path, "Chrome executable")
    validate_path(user_data_dir, "Chrome user data directory")

    profile_path = os.path.join(user_data_dir, profile_name)
    if not os.path.isdir(profile_path):
        raise FileNotFoundError(
            f"Chrome profile không tồn tại trong user data dir: {profile_path}."
            " Kiểm tra tên profile-directory hoặc profile folder."  # noqa: E501
        )

    command = build_chrome_command(url, chrome_path, user_data_dir, profile_name)
    print("Đang mở Chrome với profile Telegram đã đăng nhập...")
    print("Đường dẫn Chrome:", chrome_path)
    print("User Data Dir:", user_data_dir)
    print("Profile:", profile_name)
    print("URL:", url)
    subprocess.Popen(command, shell=False)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Mở Telegram mini app trên Chrome bằng profile đã đăng nhập Telegram."
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help="Link Telegram mini app web. Ví dụ: url_1.",
    )
    parser.add_argument(
        "--chrome-path",
        default=DEFAULT_CHROME_PATH,
        help="Đường dẫn tới chrome.exe. Mặc định dùng Chrome cài trên Windows.",
    )
    parser.add_argument(
        "--user-data-dir",
        default=DEFAULT_USER_DATA_DIR,
        help="Thư mục user data của Chrome. Mặc định %LOCALAPPDATA%\\Google\\Chrome\\User Data.",
    )
    parser.add_argument(
        "--profile-name",
        default=DEFAULT_PROFILE_NAME,
        help="Tên profile Chrome đã login Telegram, ví dụ Default hoặc Profile 1.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        open_telegram_mini_app(args.url, args.chrome_path, args.user_data_dir, args.profile_name)
    except FileNotFoundError as exc:
        print(f"Lỗi: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
