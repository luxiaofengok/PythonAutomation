from web_source import (
    create_firefox_driver,
    check_and_login,
    login_with_google,
    find_element_by_selectors,
    click_element_safe,
    FIREFOX_PROFILES,
    run_all_batches,
    run_batch
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# ==================== CONFIGURATION ====================
NASUN_URL = "https://nasun.io/"
PADO_URL = "https://pado.finance/"
GOSTOP_URL = "https://gostop.app/"

# ========================================================
def access_nasun(driver, profile_index):
    """Step N1: Access https://nasun.io/"""
    try:
        print(f"[Profile {profile_index}] [N1] Accessing {NASUN_URL}...")
        driver.get(NASUN_URL)

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

def click_login_and_google_nasun(driver, profile_index):
    """Step N2: Click login button, then login with Google (handle popup)"""
    print(f"[Profile {profile_index}] [N2] Starting login process...")
    # Find and click login button
    login_selectors = [
        "//*[@id='main-content']/section[1]/div/div/div/button",
        "//button[contains(., 'Open App')]",
    ]
    login_clicked = find_element_by_selectors(driver, login_selectors, 5)
    if not login_clicked:
        print(f"[Profile {profile_index}] [N2] Failed to click login button")
        return False
    click_element_safe(driver, login_clicked)

    time.sleep(5)
    # Handle Google login popup
    login_with_google(driver, profile_index)
    time.sleep(30)  # Wait for login to complete
    close_selectors = [
        "/html/body/div[2]/div[2]/div/div[3]/div[4]/button",
        "//button[contains(., 'Close')]",
    ]
    close_button = find_element_by_selectors(driver, close_selectors, 10)
    if close_button:
        click_element_safe(driver, close_button)
        time.sleep(2)  # Wait for any post-login actions to complete

    return True

def check_in_nasun(driver, profile_index):
    claim_selectors = [
        "//*[@id='main-content']/div[1]/div[2]/main/div/div[2]/div/div[2]/div[2]/div/div/div[3]/div[1]/div[2]/div/button",
        "//button[contains(., 'Claim All Tokens')]",
    ]
    claim_button = find_element_by_selectors(driver, claim_selectors, 10)
    if claim_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", claim_button) 
        click_element_safe(driver, claim_button)
        time.sleep(15)  # Wait for any post-login actions to complete
    print(f"[Profile {profile_index}] [N3] Claim button clicked successfully")

    mission_1_selectors = [
        "//*[@id='main-content']/div[1]/div[2]/main/div/div[2]/div/div[2]/div[3]/div/ul/li[1]/div[2]/button",
    ]
    mission_1_button = find_element_by_selectors(driver, mission_1_selectors, 10)
    if mission_1_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mission_1_button)  # Scroll to the mission 1 button
        click_element_safe(driver, mission_1_button)
    
    check_1_selectors = [
        # "/html/body/div[4]/div[2]/ul/li[2]/label/div/span[1]",
        "/html/body/div[4]/div[2]/ul/li[2]/label/input",
        "(//input[@type='checkbox'])[2]",
        "//label[contains(., 'Send Token')]",

    ]
    check_1 = find_element_by_selectors(driver, check_1_selectors, 10)
    if check_1 and check_1.is_enabled() and check_1.is_selected():
        click_element_safe(driver, check_1)
        time.sleep(1)  # Wait for any post-login actions to complete
    
    close_1_selectors = [
        # "/html/body/div[4]/div[1]/button",
        # "//button[contains(., 'Close')]",
        "//button[@aria-label='Close']",

    ]
    close_1_button = find_element_by_selectors(driver, close_1_selectors, 10)
    if close_1_button:
        click_element_safe(driver, close_1_button)
        time.sleep(2)  # Wait for any post-login actions to complete
    
    mission_2_selectors = [
        "//*[@id='main-content']/div[1]/div[2]/main/div/div[2]/div/div[2]/div[3]/div/ul/li[2]/div[2]/button",
    ]
    mission_2_button = find_element_by_selectors(driver, mission_2_selectors, 10)
    if mission_2_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mission_2_button)  # Scroll to the mission 2 button
        click_element_safe(driver, mission_2_button)
    
    check_2_selectors = [
        "/html/body/div[4]/div[2]/ul/li[2]/label/input",
        "(//input[@type='checkbox'])[2]",
        # "//label[contains(., 'Predict')]",
    ]
    check_2 = find_element_by_selectors(driver, check_2_selectors, 10)
    if check_2 and check_2.is_enabled() and not check_2.is_selected():
        click_element_safe(driver, check_2)
        time.sleep(1)  # Wait for any post-login actions to complete
    
    close_2_selectors = [
        # "/html/body/div[4]/div[1]/button",
        # "//button[contains(., 'Close')]",
        "//button[@aria-label='Close']",

    ]
    close_2_button = find_element_by_selectors(driver, close_2_selectors, 10)
    if close_2_button:
        click_element_safe(driver, close_2_button)
        time.sleep(2)  # Wait for any post-login actions to complete
    
    mission_3_selectors = [
        "//*[@id='main-content']/div[1]/div[2]/main/div/div[2]/div/div[2]/div[3]/div/ul/li[3]/div[2]/button",
    ]
    mission_3_button = find_element_by_selectors(driver, mission_3_selectors, 10)
    if mission_3_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mission_3_button)  # Scroll to the mission 3 button
        click_element_safe(driver, mission_3_button)
    
    check_3_selectors = [
        "/html/body/div[4]/div[2]/ul/li[4]/label/input",
        "//input[@type='checkbox'][4]",
        "//label[contains(., 'Play Mines')]",
    ]
    check_3 = find_element_by_selectors(driver, check_3_selectors, 10)
    if check_3 and check_3.is_enabled() and not check_3.is_selected():
        click_element_safe(driver, check_3)
        time.sleep(1)  # Wait for any post-login actions to complete
    
    close_3_selectors = [
        # "/html/body/div[4]/div[1]/button",
        # "//button[contains(., 'Close')]",
        "//button[@aria-label='Close']",

    ]
    close_3_button = find_element_by_selectors(driver, close_3_selectors, 10)
    if close_3_button:
        click_element_safe(driver, close_3_button)
        time.sleep(2)  # Wait for any post-login actions to complete
    
    time.sleep(2)
    
    stake_selectors = [
        "//*[@id='main-content']/div[1]/div[2]/main/div/div[2]/div/div[2]/div[5]/ul/li[1]/div[2]/button",
        "//button[contains(., 'Stake')]",
    ]
    stake_button = find_element_by_selectors(driver, stake_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", stake_button)  # Scroll to the stake button
    time.sleep(2)  # Wait for any scrolling animations to finish
    if not stake_button:
        print(f"[Profile {profile_index}] [N3] Stake button not found - might need to claim first")
        return False  # Coi như thất bại nếu không tìm thấy nút stake
    click_element_safe(driver, stake_button)

    validator_selectors = [
        "//*[@id='radix-_r_58_']/div/div[3]/div/div/button[1]/div/div[1]/span",
        "//span[contains(., 'validator-0')]",
    ]
    validator_button = find_element_by_selectors(driver, validator_selectors, 10)
    if not validator_button:
        print(f"[Profile {profile_index}] [N3] Validator button not found - might need to claim first")
        return False  # Coi như thất bại nếu không tìm thấy nút validator   
    click_element_safe(driver, validator_button)
    sendkey_selectors = [
        "//*[@id='radix-_r_58_']/div/div[3]/div/div[3]/input",
        "//input[@placeholder='0.0']",
    ]
    sendkey_input = find_element_by_selectors(driver, sendkey_selectors, 10)
    if not sendkey_input:
        print(f"[Profile {profile_index}] [N3] Send key input not found - might need to claim first")
        return False  # Coi như thất bại nếu không tìm thấy input gửi key   
    sendkey_input.send_keys("18")
    time.sleep(2)
    continue_selectors = [
        "//*[@id='radix-_r_58_']/div/div[3]/div/button",
        "//button[contains(., 'Continue')]",
    ]
    continue_button = find_element_by_selectors(driver, continue_selectors, 10)
    if not continue_button:
        print(f"[Profile {profile_index}] [N3] Continue button not found - might need to claim first")
        return False  # Coi như thất bại nếu không tìm thấy nút continue
    click_element_safe(driver, continue_button)

    confirm_selectors = [
        "//*[@id='radix-_r_58_']/div/div[3]/div/div[3]/button[2]",
        "//button[contains(., 'Confirm Stake')]",
    ]
    confirm_button = find_element_by_selectors(driver, confirm_selectors, 10)
    if confirm_button:
        click_element_safe(driver, confirm_button)
        time.sleep(10)
    print(f"[Profile {profile_index}] [N3] Staking process completed successfully")

    close_selectors = [
        "//*[@id='radix-_r_1u_']/button/span",
        "//span[contains(., 'Close')]",
    ]
    close_button = find_element_by_selectors(driver, close_selectors, 10)
    if close_button:
        click_element_safe(driver, close_button)
        time.sleep(2)  # Wait for any post-login actions to complete

    return True

def check_in_pado(driver, profile_index):
    main_window = driver.current_window_handle
    href_selectors = [
        "//*[@id='main-content']/div[1]/div[2]/main/div/div[2]/div/div[2]/div[2]/div/div/div[3]/div[2]/div[1]/a",
        "//a[contains(., 'Spot Trade')]",
    ]
    href_button = find_element_by_selectors(driver, href_selectors, 10)
    if href_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", href_button)  # Scroll to the link button
        time.sleep(2)  # Wait for any scrolling animations to finish
        click_element_safe(driver, href_button)
        time.sleep(5)  # Wait for new tab to open
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    # Wait for page to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    time.sleep(2)
    login_selectors = [
        "//*[@id='root']/div/main/div/div[1]/div/div[3]/div/div/button/span",
        "//span[contains(., 'Get Started')]",
    ]
    login_clicked = find_element_by_selectors(driver, login_selectors, 5)
    if login_clicked:      
        click_element_safe(driver, login_clicked)
        time.sleep(5)
        login_with_google(driver, profile_index)
        time.sleep(30)  # Wait for login to complete

    spot_selectors = [
        "//*[@id='root']/div/header/div/nav/a[1]",
        "//a[contains(., 'Spot')]",
    ]
    spot_button = find_element_by_selectors(driver, spot_selectors, 10)
    if spot_button:
        click_element_safe(driver, spot_button)
        time.sleep(2)  # Wait for any post-login actions to complete

    skip_selectors = [
        "/html/body/div/div/main/div/div[6]/div[2]/div[2]/button[1]",
        "//button[contains(., 'Skip')]",
    ]
    skip_button = find_element_by_selectors(driver, skip_selectors, 10)
    if skip_button:
        click_element_safe(driver, skip_button)
        time.sleep(2)  # Wait for any post-login actions to complete
    
    enable_selectors = [
        "/html/body/div/div/main/div/div[3]/div[3]/div[1]/button",
        "//button[contains(., 'Enable Pado')]",
    ]
    enable_button = find_element_by_selectors(driver, enable_selectors, 10)
    if enable_button:
        click_element_safe(driver, enable_button)
        time.sleep(12)  # Wait for any post-login actions to complete

    mid_selectors = [
        "//*[@id='root']/div/main/div/div[3]/div[3]/div[1]/div/div/div[1]/div[4]/div[1]/div/button[1]",
        "//button[contains(., 'Mid')]",
    ]
    mid_button = find_element_by_selectors(driver, mid_selectors, 10)
    if mid_button:
        click_element_safe(driver, mid_button)
        time.sleep(1)  # Wait for any post-login actions to complete
    
    percent_selectors = [
        "//*[@id='root']/div/main/div/div[3]/div[3]/div[1]/div/div/div[1]/div[5]/div[3]/button[2]",
        "//button[contains(., '50%')]",
    ]
    percent_button = find_element_by_selectors(driver, percent_selectors, 10)
    if percent_button:
        click_element_safe(driver, percent_button)
        time.sleep(1)  # Wait for any post-login actions to complete
  

    buy_selectors = [
        "//*[@id='root']/div/main/div/div[3]/div[3]/div[1]/div/div/div[1]/button",
        "//button[contains(., 'Buy NBTC')]",
    ]
    buy_button = find_element_by_selectors(driver, buy_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_button)  # Scroll to the buy button
    time.sleep(2)  # Wait for any scrolling animations to finish
    if buy_button:
        click_element_safe(driver, buy_button)
        time.sleep(1)  # Wait for any post-login actions to complete

    checkbox_selectors = [
        "//*[@id='root']/div/main/div/div[3]/div[3]/div[1]/div/div/div[3]/div[2]/div[2]/label/span",
        "//span[contains(., 'Don't show again (enable one-click trading)')]",
    ]
    checkbox = find_element_by_selectors(driver, checkbox_selectors, 10)
    if checkbox:
        click_element_safe(driver, checkbox)
        time.sleep(1)  # Wait for any post-login actions to complete
    
    confirm_selectors = [
        "//*[@id='root']/div/main/div/div[5]/div[2]/div[3]/div/div/div[3]/div[2]/div[2]/div[3]/button[2]",
        "//button[contains(., 'Confirm Buy')]",
    ]
    confirm_button = find_element_by_selectors(driver, confirm_selectors, 10)
    if confirm_button:
        click_element_safe(driver, confirm_button)

    time.sleep(20)

    predict_selectors = [
        "/html/body/div[1]/div/header/div/nav/a[2]",
        "//*[@id='root']/div/header/div/nav/a[2]",
        "//a[contains(., 'Predict')]",
    ]
    predict_button = find_element_by_selectors(driver, predict_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", predict_button)  # Scroll to the predict button
    time.sleep(2)  # Wait for any scrolling animations to finish
    if predict_button:
        click_element_safe(driver, predict_button)

    icon_selectors = [
        "//*[@id='root']/div/main/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/a/div[2]/p[1]",

    ]
    icon_button = find_element_by_selectors(driver, icon_selectors, 10)
    if icon_button:
        click_element_safe(driver, icon_button)
        time.sleep(1)  # Wait for any post-login actions to complete
    input_selectors = [
        "//*[@id='trade-form']/div[1]/div/form/div/input",
        "//input[@placeholder='0.00']",
    ]
    input_field = find_element_by_selectors(driver, input_selectors, 10)
    if input_field:
        input_field.send_keys("88")
        time.sleep(1)
    buy_predict_selectors = [
        "//*[@id='trade-form']/div[1]/div/form/button",
        "//button[contains(., 'Buy YES')]",
    ]
    buy_predict_button = find_element_by_selectors(driver, buy_predict_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_predict_button)  # Scroll to the buy predict button
    time.sleep(1)  # Wait for any scrolling animations to finish
    if buy_predict_button:
        click_element_safe(driver, buy_predict_button)
        time.sleep(1)
    got_it_selectors = [
        "/html/body/div[3]/div/button",
        "//button[contains(., 'Got it')]",
    ]
    got_it_button = find_element_by_selectors(driver, got_it_selectors, 10)
    if got_it_button:
        click_element_safe(driver, got_it_button)
        time.sleep(1)  # Wait for any post-login actions to complete
    time.sleep(15)  # Wait for any post-login actions to complete

    no_selectors = [
        "//*[@id='trade-form']/div[1]/div/div[3]/button[2]",
        "//button[contains(., 'No')]",
    ]
    no_button = find_element_by_selectors(driver, no_selectors, 10)
    if no_button:
        click_element_safe(driver, no_button)
        time.sleep(1)  # Wait for any post-login actions to complete
    
    input_selectors = [
        "//*[@id='trade-form']/div[1]/div/form/div/input",
        "//input[@placeholder='0.00']",
    ]
    input_field = find_element_by_selectors(driver, input_selectors, 10)
    if input_field:
        input_field.send_keys("88")
        time.sleep(1)
    
    buy_no_selectors = [
        "//*[@id='trade-form']/div[1]/div/form/button",
        "//button[contains(., 'Buy NO')]",
    ]
    buy_no_button = find_element_by_selectors(driver, buy_no_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy_no_button)  # Scroll to the buy no button
    time.sleep(1)  # Wait for any scrolling animations to finish
    if buy_no_button:
        click_element_safe(driver, buy_no_button)
        time.sleep(1)  # Wait for any post-login actions to complete
    
    got_it_selectors = [
        "/html/body/div[3]/div/button",
        "//button[contains(., 'Got it')]",
    ]
    got_it_button = find_element_by_selectors(driver, got_it_selectors, 10)
    if got_it_button:
        click_element_safe(driver, got_it_button)
        time.sleep(1)  # Wait for any post-login actions to complete
    time.sleep(15)  # Wait for any post-login actions to complete


    driver.close()  # Close the Pado tab
    time.sleep(2)
    driver.switch_to.window(main_window)  # Switch back to the main tab
    return True

def check_in_gostop(driver, profile_index):
    main_window = driver.current_window_handle
    href_selectors = [
        "//*[@id='main-content']/div[1]/div[2]/main/div/div[2]/div/div[2]/div[2]/div/div/div[3]/div[4]/div[1]/a",
        "//a[contains(., 'Buy Lottery Ticket')]",
    ]
    href_button = find_element_by_selectors(driver, href_selectors, 10)
    if href_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", href_button)  # Scroll to the link button
        time.sleep(2)  # Wait for any scrolling animations to finish
        click_element_safe(driver, href_button)
        time.sleep(5)  # Wait for new tab to open
    
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    # Wait for page to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    time.sleep(2)
    login_selectors = [
        "//*[@id='root']/div/header/div/div/div[1]/div/button/span",
        "//span[contains(., 'Get Started')]",
    ]
    login_clicked = find_element_by_selectors(driver, login_selectors, 5)
    if login_clicked:
        click_element_safe(driver, login_clicked)
        time.sleep(5)
        login_with_google(driver, profile_index)
        time.sleep(30)  # Wait for login to complete

    play_selectors = [
        "//*[@id='live']/div[2]/a[1]/span",
        "//span[contains(., 'Play')]",
    ]
    play_button = find_element_by_selectors(driver, play_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", play_button)  # Scroll to the play button
    time.sleep(1)  # Wait for any scrolling animations to finish
    if not play_button:
        print(f"[Profile {profile_index}] [G1] Play button not found - login might have failed")
        return False
    click_element_safe(driver, play_button)
    time.sleep(2)

    claim_selectors = [
        "//*[@id='root']/div/main/div/section[1]/ul/li/button",
        "//button[contains(., 'Claim')]",
    ]
    claim_button = find_element_by_selectors(driver, claim_selectors, 10)
    if claim_button:
        click_element_safe(driver, claim_button)
        time.sleep(10)  # Wait for any post-login actions to complete

    buy10_selectors = [
        "//*[@id='root']/div/main/div/section[2]/div[2]/button[3]/span[2]",
        "//span[contains(., '50.00')]",
    ]
    buy10_button = find_element_by_selectors(driver, buy10_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buy10_button)  # Scroll to the buy10 button
    time.sleep(1)  # Wait for any scrolling animations to finish
    if not buy10_button:
        print(f"[Profile {profile_index}] [G1] Buy 10 button not found - might need to click Play first")
        return False
    click_element_safe(driver, buy10_button)
    time.sleep(10)

    got_it_selectors = [
        "/html/body/div[3]/div/button",
        "//button[contains(., 'Got it')]",
    ]
    got_it_button = find_element_by_selectors(driver, got_it_selectors, 10)
    if got_it_button:
        click_element_safe(driver, got_it_button)
        time.sleep(1)
    
    gostop_selectors = [
        "//*[@id='root']/div/header/div/a/span[2]",
        "//span[contains(., 'GoStop')]",
    ]
    gostop_button = find_element_by_selectors(driver, gostop_selectors, 10)
    if gostop_button:
        click_element_safe(driver, gostop_button)
    time.sleep(1)

    scratch_selectors = [
        "//*[@id='live']/div[2]/a[2]/span",
        "//span[contains(., 'Scratch')]",
    ]
    scratch_button = find_element_by_selectors(driver, scratch_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", scratch_button)  # Scroll to the scratch button
    time.sleep(1)  # Wait for any scrolling animations to finish
    if scratch_button:
        click_element_safe(driver, scratch_button)
        time.sleep(1)  # Wait for any post-login actions to complete
    buy_scratch_selectors = [
        "//*[@id='root']/div/main/div/section[1]/div[2]/button[4]/span[2]",
        "//span[contains(., '50.00')]",
    ]
    buy_scratch_button = find_element_by_selectors(driver, buy_scratch_selectors, 10)
    if buy_scratch_button:
        click_element_safe(driver, buy_scratch_button)
        time.sleep(10)  # Wait for any post-login actions to complete
    
    reveal_selectors = [
        "//*[@id='root']/div/main/div/section[2]/div[1]/button",
        "//button[contains(., 'Reveal all')]",
    ]
    reveal_button = find_element_by_selectors(driver, reveal_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reveal_button)  # Scroll to the reveal button
    time.sleep(1)  # Wait for any scrolling animations to finish
    if reveal_button:
        click_element_safe(driver, reveal_button)
        
    close_selectors = [
        "/html/body/div[3]/div/div[3]/button[1]",
        "//button[contains(., 'Close')]",
    ]
    close_button = find_element_by_selectors(driver, close_selectors, 10)
    if close_button:
        click_element_safe(driver, close_button)
        time.sleep(1)  # Wait for any post-login actions to complete
    
    click_element_safe(driver, gostop_button)
    time.sleep(1)

    number_selectors = [
        "//*[@id='live']/div[2]/a[3]/div[2]/h3",
        "//h3[contains(., 'Number Match')]",
    ]
    number_button = find_element_by_selectors(driver, number_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", number_button)  # Scroll to the number button
    time.sleep(1)  # Wait for any scrolling animations to finish
    if number_button:
        click_element_safe(driver, number_button)
        time.sleep(1)  # Wait for any post-login actions to complete
    
    num_1_selectors = [
        "//*[@id='root']/div/main/div/section[1]/div[2]/button[1]",
        "//button[contains(., '1')]",
    ]
    num_1_button = find_element_by_selectors(driver, num_1_selectors, 10)
    if num_1_button:
        click_element_safe(driver, num_1_button)
    
    num_3_selectors = [
        "//*[@id='root']/div/main/div/section[1]/div[2]/button[3]",
        "//button[contains(., '3')]",
    ]
    num_3_button = find_element_by_selectors(driver, num_3_selectors, 10)
    if num_3_button:
        click_element_safe(driver, num_3_button)

    num_5_selectors = [
        "//*[@id='root']/div/main/div/section[1]/div[2]/button[5]",
        "//button[contains(., '5')]",
    ]
    num_5_button = find_element_by_selectors(driver, num_5_selectors, 10)
    if num_5_button:
        click_element_safe(driver, num_5_button)

    pick_play_selectors = [
        "//*[@id='root']/div/main/div/section[2]/div[2]/button",
        "//button[contains(., 'Play 3 picks')]",
    ]
    pick_play_button = find_element_by_selectors(driver, pick_play_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pick_play_button)  # Scroll to the play picks button
    time.sleep(1)  # Wait for any scrolling animations to finish
    if pick_play_button:
        click_element_safe(driver, pick_play_button)
        time.sleep(15)  # Wait for any post-login actions to complete
    
    click_element_safe(driver, gostop_button)
    time.sleep(1)

    mine_selectors = [
        "//*[@id='live']/div[2]/a[4]/span",
        "//span[contains(., 'Enter')]",
    ]
    mine_button = find_element_by_selectors(driver, mine_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mine_button)  # Scroll to the mine button
    time.sleep(1)  # Wait for any scrolling animations to finish
    if mine_button:
        click_element_safe(driver, mine_button)
        time.sleep(1)  # Wait for any post-login actions to complete
    
    start_mine_selectors = [
        "//*[@id='root']/div/main/div/section/button",
        "//button[contains(., 'Start Session · 1.00 NUSDC')]",
    ]
    start_mine_button = find_element_by_selectors(driver, start_mine_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_mine_button)  # Scroll to the start mine button
    time.sleep(1)  # Wait for any scrolling animations to finish
    if start_mine_button:
        click_element_safe(driver, start_mine_button)
        time.sleep(10)  # Wait for any post-login actions to complete

    mine_1_selectors = [
        "//*[@id='root']/div/main/div/section/div[2]/button[1]/span",
        "//span[contains(., '1')]",
    ]
    mine_1_button = find_element_by_selectors(driver, mine_1_selectors, 10)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mine_1_button)  # Scroll to the mine 1 button
    time.sleep(1)  # Wait for any scrolling animations to finish
    if mine_1_button:
        click_element_safe(driver, mine_1_button)
        time.sleep(3)  # Wait for any post-login actions to complete

    mine_7_selectors = [
        "//*[@id='root']/div/main/div/section/div[2]/button[7]/span",
        "//span[contains(., '7')]",
    ]
    mine_7_button = find_element_by_selectors(driver, mine_7_selectors, 10)
    if mine_7_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mine_7_button)  # Scroll to the mine 7 button
        time.sleep(1)  # Wait for any scrolling animations to finish
        click_element_safe(driver, mine_7_button)
        time.sleep(3)  # Wait for any post-login actions to complete
    
    mine_13_selectors = [
        "//*[@id='root']/div/main/div/section/div[2]/button[13]/span",
        "//span[contains(., '13')]",
    ]
    mine_13_button = find_element_by_selectors(driver, mine_13_selectors, 10)
    if mine_13_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mine_13_button)  # Scroll to the mine 13 button
        time.sleep(1)  # Wait for any scrolling animations to finish
        click_element_safe(driver, mine_13_button)
        time.sleep(3)  # Wait for any post-login actions to complete
    
    mine_19_selectors = [
        "//*[@id='root']/div/main/div/section/div[2]/button[19]/span",
        "//span[contains(., '19')]",
    ]
    mine_19_button = find_element_by_selectors(driver, mine_19_selectors, 10)
    if not mine_19_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mine_19_button)  # Scroll to the mine 19 button
        time.sleep(1)  # Wait for any scrolling animations to finish
        click_element_safe(driver, mine_19_button)
        time.sleep(3)  # Wait for any post-login actions to complete

    mine_25_selectors = [
        "//*[@id='root']/div/main/div/section/div[2]/button[25]/span",
        "//span[contains(., '25')]",
    ]
    mine_25_button = find_element_by_selectors(driver, mine_25_selectors, 10)
    if mine_25_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mine_25_button)  # Scroll to the mine 25 button
        time.sleep(1)  # Wait for any scrolling animations to finish
        click_element_safe(driver, mine_25_button)
        time.sleep(3)  # Wait for any post-login actions to complete

    cashout_selectors = [
        "//*[@id='root']/div/main/div/section/div[3]/button",
        "//button[contains(., 'Cash Out · 1.96 NUSDC')]",
    ]
    cashout_button = find_element_by_selectors(driver, cashout_selectors, 10)
    if not cashout_button:
        return False  # Coi như thất bại nếu không tìm thấy nút cashout

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cashout_button)  # Scroll to the cashout button
    time.sleep(1)  # Wait for any scrolling animations to finish
    click_element_safe(driver, cashout_button)
    time.sleep(10)  # Wait for any post-login actions to complete
    driver.close()  # Close the GoStop tab
    time.sleep(2)
    driver.switch_to.window(main_window)  # Switch back to the main tab
    time.sleep(15) 
    driver.refresh()  # Refresh the main page to update any changes from GoStop
    time.sleep(20)  # Wait for refresh to complete
    play_numbers_selectors = [
        "//*[@id='main-content']/div[1]/div[2]/main/div/div[2]/div/div[2]/div[2]/div/div/div[3]/div[6]/div[1]/a",
        "//a[contains(., 'Play Number Match')]",
    ]
    play_numbers_button = find_element_by_selectors(driver, play_numbers_selectors, 10)
    if play_numbers_button:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", play_numbers_button)  # Scroll to the play numbers button
        time.sleep(5)  # Wait for any post-login actions to complete
    
    return True
 

def run_nasun_script(profile_path, profile_index):
    """Chạy automation script cho NASUN"""
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"\n[Profile {profile_index}] Starting NASUN automation...")
        print(f"{'='*60}")
        driver = create_firefox_driver(profile_path)
        
        if not access_nasun(driver, profile_index):
            return False
        
        if not click_login_and_google_nasun(driver, profile_index):
            return False
        
        if not check_in_nasun(driver, profile_index):
            return False
        
        if not check_in_pado(driver, profile_index):
            return False
        
        if not check_in_gostop(driver, profile_index):
            return False
        
        print(f"[Profile {profile_index}] NASUN automation completed successfully")
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
    # run_nasun_script(FIREFOX_PROFILES[0],1)
    # run_batch(
    # [
    #     (FIREFOX_PROFILES[0], 1),
    #     (FIREFOX_PROFILES[1], 2),
    #     (FIREFOX_PROFILES[5], 6),
    #     (FIREFOX_PROFILES[21], 22)
    # ],
    # batch_num=1,
    # task_function=run_nasun_script,
    # max_workers=4
    # )
    results = run_all_batches(run_nasun_script, FIREFOX_PROFILES)
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




