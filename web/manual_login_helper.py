import subprocess
import time

FIREFOX_PATH = r"C:\Program Files\Mozilla Firefox\firefox.exe"
PROFILES_DIR = r"C:\Users\Admin\AppData\Roaming\Mozilla\Firefox\Profiles"
TARGET_URL = "https://waitlist.kindredlabs.ai/dashboard"

PROFILES = [
    # "EYFYwuoC.Profile 1",
    # "K7Ms67Yf.Hồ sơ 2",
    # "jmCZhbq0.Hồ sơ 3",
    # "hVlpgpyW.Hồ sơ 4",
    # "EYUavWHf.Hồ sơ 5",
    # "gA6pOEMK.Hồ sơ 6",
    # "rPhWDpKS.Hồ sơ 7",
    # "BGU2Szlj.Hồ sơ 8",
    # "9bThzlN5.Hồ sơ 9",
    # "1o3VePEW.Hồ sơ 10",
    # "wt1JsR72.Hồ sơ 11",
    # "r2LAx6mT.Hồ sơ 12",
    # "XNaxUADk.Hồ sơ 13",
    # "edPXdFYz.Hồ sơ 14",
    # "91PbC0aX.Hồ sơ 15",
    # "kxLMQ7uV.Hồ sơ 16",
    # "j09dZ5W6.Hồ sơ 17",
    # "VrxQR82t.Hồ sơ 18",
    # "WVZoasKN.Hồ sơ 19",
    # "Y2YfF82j.Hồ sơ 20",
    # "fLKSCXiH.Hồ sơ 21",
    # "8LrfqVIk.Hồ sơ 22",
]

def open_profile_for_login(profile_name, index):
    """Open Firefox with specific profile for manual login"""
    profile_path = f"{PROFILES_DIR}\\{profile_name}"
    
    print(f"\n{'='*60}")
    print(f"Opening Profile {index}: {profile_name}")
    print(f"{'='*60}")
    print(f"1. Browser will open")
    print(f"2. Login to the website manually")
    print(f"3. Complete any tasks if needed")
    print(f"4. Close the browser when done")
    print(f"{'='*60}\n")
    
    try:
        # Open Firefox with the profile
        subprocess.run([
            FIREFOX_PATH,
            "-profile", profile_path,
            TARGET_URL
        ])
        
        print(f"\n✅ Profile {index} closed")
        
    except Exception as e:
        print(f"❌ Error opening profile {index}: {e}")

def main():
    print("="*60)
    print("Firefox Profile Manual Login Helper")
    print("="*60)
    print(f"Total profiles: {len(PROFILES)}")
    print(f"URL: {TARGET_URL}")
    print("="*60)
    print("\nEach profile will open one by one.")
    print("Login manually, then close the browser to continue.\n")
    
    input("Press Enter to start...")
    
    for i, profile in enumerate(PROFILES, 1):
        open_profile_for_login(profile, i)
        
        if i < len(PROFILES):
            print(f"\nReady for next profile...")
            time.sleep(2)
    
    print("\n" + "="*60)
    print("ALL PROFILES COMPLETED!")
    print("="*60)
    print("\nNow you can run: python web_kindredlab.py")
    print("The script will use saved cookies and bypass Cloudflare!")
    print("="*60)

if __name__ == "__main__":
    main()
