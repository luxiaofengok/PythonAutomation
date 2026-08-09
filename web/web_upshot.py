"""Upshot Cards Automation - Login and button clicks"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
from time import sleep
import sys
sys.path.append('c:\\PythonAutomation')
from web.web_source import (
    create_firefox_driver,
    find_element_by_selectors,
    click_element_safe,
    cleanup_all,
    run_all_batches,
    FIREFOX_PROFILES
)

# ==================== CONFIGURATION ====================
URL = "https://upshot.cards/claim"
WAIT_AFTER_LOGIN = 30  # Tăng từ 10 lên 15
# ======================================================


def upshot_task(profile_path, profile_index):
    """Main task for Upshot Cards automation"""
    driver = None
    try:
        print(f"\n[Profile {profile_index}] Starting Upshot automation...")
        
        # Create driver and navigate
        driver = create_firefox_driver(profile_path,headless=False)
        driver.get(URL)
        time.sleep(20)  # Tăng từ 5 lên 7
        driver.refresh()
        time.sleep(20)  # Tăng từ 5 lên 7
        
        # Try to click initial button
        try:
            initial_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[2]/button"))
            )
            initial_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"[Profile {profile_index}] Initial button not found or already clicked: {str(e)}")
        
        # Step 1: Click Google login button in modal
        print(f"[Profile {profile_index}] Step 1: Looking for Google login button...")
        google_selectors = [
            "//button[contains(., 'Continue with Google')]",
            "//button[contains(., 'Google')]",
            "//button[contains(., 'Sign in with Google')]",
            "//*[contains(@class, 'google')]//button",
            "//button[.//text()[contains(., 'Google')]]"
        ]
        
        google_button = find_element_by_selectors(driver, google_selectors, wait_time=10)
        if google_button:
            driver.execute_script("arguments[0].scrollIntoView(true);", google_button)
            time.sleep(3)  # Tăng từ 1 lên 3
            google_button.click()
            print(f"[Profile {profile_index}] Clicked Google login button")
            time.sleep(7)  # Tăng từ 5 lên 7
            
            # Select Google account
            account_selectors = [
                "//li[1]//div[@role='link']",
                "//div[@data-authuser='0']",
                "//ul//li[1]//div[contains(@class, 'BHzsHc')]",
                "(//div[contains(@jsname, 'V67aGc')])[1]"
            ]
            
            google_account = find_element_by_selectors(driver, account_selectors, wait_time=5)
            if google_account:
                google_account.click()
                print(f"[Profile {profile_index}] Selected Google account")
                time.sleep(5)  # Tăng từ 3 lên 5
            
            # Wait after login
            print(f"[Profile {profile_index}] Waiting {WAIT_AFTER_LOGIN}s after login...")
            time.sleep(WAIT_AFTER_LOGIN)
        else:
            print(f"[Profile {profile_index}] Google login button not found, may already be logged in")


        # Step 2: Close modal by clicking X button
        print(f"[Profile {profile_index}] Step 2: Closing modal...")
        close_selectors = [
            "//button[contains(@class, 'close') or contains(@aria-label, 'close') or contains(@aria-label, 'Close')]",
            "//button[text()='×' or text()='X']",
            "//*[@role='button'][text()='×' or text()='X']",
            "//button[contains(., '×')]"
        ]
        
        close_button = find_element_by_selectors(driver, close_selectors, wait_time=5)
        if close_button:
            click_element_safe(driver, close_button)
            print(f"[Profile {profile_index}] Modal closed")
            time.sleep(4)  # Tăng từ 2 lên 4
        else:
            print(f"[Profile {profile_index}] Close button not found, modal may have auto-closed")
        sleep(20)  # Tăng từ 3 lên 5
        action = ActionChains(driver)
        action.move_to_element_with_offset(driver.find_element(By.TAG_NAME, 'body'), 10, 10).perform()
        sleep(5)  # Tăng từ 2 lên 5

        got_it_selectors= [
            "//*[@id='radix-_r_0_']/div[2]/button",
            "//*[@id='radix-_r_0_']/div[2]/button/span",
            "//span[contains(., 'Got it')]",
        ]
        got_it_button = find_element_by_selectors(driver,got_it_selectors,5)
        if got_it_button:
            click_element_safe(driver,got_it_button)
            time.sleep(2)
       
        # Step 3: Click Claim button
        print(f"[Profile {profile_index}] Step 3: Clicking Claim button...")
        try:
            claim_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/img"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", claim_button)
            time.sleep(3)
            click_element_safe(driver, claim_button)
            print(f"[Profile {profile_index}] Clicked Claim button")
            time.sleep(4)
        except Exception as e:
            print(f"[Profile {profile_index}] Error clicking Claim button: {str(e)}")
            # driver.refresh()
            # time.sleep(20)
            # claim_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/div/div/div/div[1]/img"))
            # )
            # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", claim_button)
            # time.sleep(3)
            # click_element_safe(driver, claim_button)
            # print(f"[Profile {profile_index}] Clicked Claim button")
            # time.sleep(4)
        
        # Step 4: Click Continue button
        print(f"[Profile {profile_index}] Step 4: Clicking Continue button...")
        try:
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div[2]/div[1]/div[2]/div/div/div[3]/button/span"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_button)
            time.sleep(5)
            click_element_safe(driver, continue_button)
            print(f"[Profile {profile_index}] Clicked Continue button")
            time.sleep(4)
        except Exception as e:
            print(f"[Profile {profile_index}] Error clicking Continue button: {str(e)}")
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div[2]/div[1]/div[2]/div/button/span"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_button)
            time.sleep(5)
            click_element_safe(driver, continue_button)
            print(f"[Profile {profile_index}] Clicked Continue button")
        print(f"[Profile {profile_index}] Task completed successfully!")
        time.sleep(10)  # Tăng từ 3 lên 5

        try:
            claim_reward_selectors = [
                "//span[contains(., 'Claim Reward')]",
                "/html/body/div[4]/main/div/div[1]/div/div[2]/div/div[1]/div/div/div[2]/button/span[2]",
            ]
            claim_reward_button = find_element_by_selectors(driver, claim_reward_selectors, wait_time=5)

            if claim_reward_button:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", claim_reward_button)
                time.sleep(1)
                click_element_safe(driver, claim_reward_button)
                time.sleep(10)

            # follow_X_selectors=[
            #     "/html/body/div[4]/main/div/div[1]/div/div[2]/div/div/div[2]/div[7]/div/div[2]/div[2]/button/span",
            #     "span[contains(., 'Follow')]",
            # ]
            # follow_X_button= find_element_by_selectors(driver,follow_X_selectors,wait_time=5)
            # if follow_X_button:
            #     main_window = driver.current_window_handle
            #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", follow_X_button)
            #     time.sleep(1)
            #     click_element_safe(driver,follow_X_button)
            #     time.sleep(1)
            #     for handle in driver.window_handles:
            #         if handle!= main_window:
            #             driver.switch_to.window(handle)
            #             break
            #     time.sleep(3)
            #     driver.close()
            #     time.sleep(2)
            #     driver.switch_to.window(main_window)
            #     time.sleep(3)

            # follow_instagram_selectors=[
            #     "/html/body/div[4]/main/div/div[1]/div/div[2]/div/div/div[2]/div[7]/div/div[2]/div[2]/button/span",
            #     "span[contains(., 'Follow')]",
            # ]
            # follow_instagram_button= find_element_by_selectors(driver,follow_instagram_selectors,wait_time=5)
            # if follow_instagram_button:
            #     main_window = driver.current_window_handle
            #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", follow_instagram_button)
            #     time.sleep(1)
            #     click_element_safe(driver,follow_instagram_button)
            #     time.sleep(1)
            #     for handle in driver.window_handles:
            #         if handle!= main_window:
            #             driver.switch_to.window(handle)
            #             break
            #     time.sleep(3)
            #     driver.close()
            #     time.sleep(2)
            #     driver.switch_to.window(main_window)
            #     time.sleep(3)

            # sell_card_selectors=[
            #     "/html/body/div[4]/main/div/div[1]/div/div[2]/div/div[2]/div[2]/div[9]/div/div[2]/div[2]/a/span",
            #     "//span[contains(., 'Sell a Card')]",
            # ]
            # sell_card_button = find_element_by_selectors(driver,sell_card_selectors,wait_time=5)

            # if sell_card_button:
            #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sell_card_button)
            #     time.sleep(1)
            #     click_element_safe(driver, sell_card_button)
            #     time.sleep(1)
            #     time.sleep(5)

            My_collection_selectors = [
                "/html/body/div[4]/main/div/div[1]/div/div[1]/div/div/div[2]",
                "//div[contains(., 'My Collection')]",
                
            ]
            My_collection_button = find_element_by_selectors(driver,My_collection_selectors,5)
            if My_collection_button:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", My_collection_button)
                time.sleep(1)
                click_element_safe(driver,My_collection_button)
                time,sleep(2)

            image_selectors=[
                "/html/body/div[4]/main/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]/div/a[1]/div/div[1]/div[1]/img[2]",
                
            ]
            click_image = find_element_by_selectors(driver,image_selectors,wait_time=5)

            if click_image:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", click_image)
                time.sleep(1)
                click_element_safe(driver,click_image)
                time.sleep(1)
                time.sleep(5)
            # buy_now_selectors=[
            #     "/html/body/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button/span",
            #     "//span[contains(., 'Buy now')]",
            # ]
            # buy_now_button= find_element_by_selectors(driver,buy_now_selectors,wait_time=5)
            # if buy_now_button:
            #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_now_button)
            #     time.sleep(1)
            #     click_element_safe(driver,buy_now_button)
            #     time.sleep(1)

            # confirm_buy_selectors=[
            #     "//div[@role='dialog']//button[.//span[normalize-space()='Buy now']]",
            #     "//div[@role='dialog']//span[normalize-space()='Buy now']/ancestor::button",
            # ]
            # confirm_buy_button=find_element_by_selectors(driver,confirm_buy_selectors,wait_time=5)
            # if confirm_buy_button:
            #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_now_button)
            #     time.sleep(1)
            #     click_element_safe(driver,buy_now_button)
            #     time.sleep(1)
            #     time.sleep(3)

            sell_selectors =[
                "/html/body/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[1]/button[2]",
                "//button[contains(., 'Sell')]",
            ]
            sell_button= find_element_by_selectors(driver,sell_selectors,wait_time=5)
            if sell_button:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sell_button)
                time.sleep(1)
                click_element_safe(driver,sell_button)
                time.sleep(1)
            sell_this_card_selectors=[
                "/html/body/div[4]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/button/span",
                "//span[contains(., 'Sell this card')]",
            ]
            sell_this_card_button= find_element_by_selectors(driver,sell_this_card_selectors,wait_time=5)
            if sell_this_card_button:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sell_this_card_button)
                time.sleep(1)
                click_element_safe(driver,sell_this_card_button)
                time.sleep(1)
            sell=[
                "//div[@role='dialog']//button[.//span[normalize-space()='Sell']]",
                "//div[@role='dialog']//span[normalize-space()='Sell']/ancestor::button",
            ]
            confirm_sell_button=find_element_by_selectors(driver,sell,wait_time=5)
            if confirm_sell_button:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_sell_button)
                time.sleep(2)
                click_element_safe(driver,confirm_sell_button)
                time.sleep(1)
                time.sleep(3)

            dashboard_selectors=[
                "/html/body/div[2]/div/div/div[1]/div/div[2]/a[1]/span",
                "//span[contains(., 'Dashboard')]",
            ]
            dashboard_button=find_element_by_selectors(driver,dashboard_selectors,wait_time=5)
            if dashboard_button:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dashboard_button)
                time.sleep(1)
                click_element_safe(driver,dashboard_button)
                time.sleep(1)
            time.sleep(2)

            for i in range(5):
                try:

                    claim_prize_1_selectors=[
                        "/html/body/div[4]/main/div/div[2]/div[1]/section/div[2]/div[2]/div/div[1]/a/div/div[2]/div/button/span[2]",
                        "//span[contains(., 'Claim Prize')]"
                    ]
                    claim_prize_1_button = find_element_by_selectors(driver,claim_prize_1_selectors, wait_time=5)

                    if not claim_prize_1_button:
                        return False
                    
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", claim_prize_1_button)
                    time.sleep(1)
                    click_element_safe(driver, claim_prize_1_button)
                    time.sleep(3)

                    confirm_1_selectors=[
                        "//div[@role='dialog']//button[.//span[normalize-space()='Claim Prize']]",
                        "//div[@role='dialog']//span[normalize-space()='Claim Prize']/ancestor::button",
                    ]
                    confirm_1_button= find_element_by_selectors(driver, confirm_1_selectors, wait_time=5)

                    if confirm_1_button:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_1_button)
                        time.sleep(1)
                        click_element_safe(driver, confirm_1_button)
                        time.sleep(1)

                    time.sleep(10)
                except Exception as e:
                    print(f"[Profile {profile_index}] No Claim Prize button or error during claiming: {str(e)}")


            
        except Exception as e:
            print(f"[Profile {profile_index}] No Claim Prize button or error during claiming: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"[Profile {profile_index}] Error: {str(e)}")
        return False
        
    finally:
        if driver:
            driver.quit()
        cleanup_all(profile_path, profile_index)


def main():

    """Run automation for all profiles in batches"""
    print("="*60)
    print("UPSHOT CARDS AUTOMATION")
    print("="*60)
    print(f"URL: {URL}")
    print(f"Total profiles: {len(FIREFOX_PROFILES)}")
    print("="*60)

    # Run all batches (8+8+6 profiles)
    results = run_all_batches(upshot_task, FIREFOX_PROFILES, wait_between_batches=8)
    #Summary
    success = sum(1 for r in results if r)
    print("\n" + "="*60)
    print(f"COMPLETED: {success}/{len(results)} profiles successful")
    print("="*60)


if __name__ == "__main__":
    main()