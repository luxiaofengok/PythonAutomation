"""AskSurf.ai Automation - Auto login and interact with AI"""

from web_source import *
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# ==================== TIMING CONFIGURATION ====================
WAIT_PAGE_LOAD = 5          # Chờ sau khi load trang
WAIT_AFTER_LOGIN = 3        # Chờ sau khi click login
WAIT_GOOGLE_LOGIN = 4       # Chờ sau khi click Google login
WAIT_ACCOUNT_SELECT = 2     # Chờ sau khi chọn tài khoản
WAIT_BEFORE_ACTION = 2      # Chờ trước khi thao tác
WAIT_AFTER_ACTION = 2       # Chờ sau khi thao tác
WAIT_AFTER_DEEP_RESEARCH = 120  # Chờ 2 phút sau deep research
WAIT_BETWEEN_INSTANT = 30   # Chờ 30 giây giữa các lần instant
WAIT_BEFORE_CLOSE = 5       # Chờ trước khi đóng browser
WAIT_BETWEEN_BATCHES = 8    # Chờ giữa các batch
ELEMENT_TIMEOUT = 30        # Timeout tìm element (giây)
INSTANT_REPEAT_COUNT = 10   # Số lần lặp instant mode
# ============================================================

ASKSURF_URL = "https://asksurf.ai/"

# Login indicators (các element chỉ báo đã login)
LOGGED_IN_INDICATORS = [
    "//textarea[@placeholder]",
    "//button[contains(@class, 'send')]",
    "//form//textarea",
]

# Suggested questions (các câu hỏi gợi ý)
SUGGESTED_QUESTIONS = [
    "What is the current state of Ethereum?",
    "Tell me about Solana ecosystem",
    "What are the top DeFi protocols?",
    "Explain Bitcoin halving",
    "What is Layer 2 scaling?",
    "How does proof of stake work?",
    "What is the difference between Bitcoin and Ethereum?",
    "Explain smart contracts",
    "What are NFTs and how do they work?",
    "Tell me about Polygon network",
    "What is Cardano?",
    "Explain decentralized exchanges",
    "What is yield farming?",
    "How does staking work in crypto?",
    "What are gas fees in Ethereum?",
    "Explain wrapped Bitcoin",
    "What is Avalanche blockchain?",
    "Tell me about Cosmos ecosystem",
    "What are DAOs?",
    "Explain liquidity pools",
    "What is Chainlink?",
    "How does Uniswap work?",
    "What is Polkadot?",
    "Explain cross-chain bridges",
    "What are stablecoins?",
    "Tell me about Arbitrum",
    "What is Optimism rollup?",
    "Explain zkSync technology",
    "What are privacy coins?",
    "How does Aave protocol work?",
    "What is Compound Finance?",
    "Explain MakerDAO",
    "What is Curve Finance?",
    "Tell me about Fantom network",
    "What are sidechains?",
    "Explain blockchain oracles",
    "What is the Lightning Network?",
    "How does Tornado Cash work?",
    "What are ERC-20 tokens?",
    "Explain MEV in Ethereum",
    "What is Lido Finance?",
    "Tell me about Binance Smart Chain",
    "What are flash loans?",
    "Explain impermanent loss",
    "What is the Ethereum merge?",
    "How does proof of work mining work?",
    "What are consensus mechanisms?",
    "Tell me about Aptos blockchain",
    "What is Sui network?",
    "Explain account abstraction",
    "What are EIP-4337 benefits?",
    "How do multisig wallets work?",
    "What is the Cosmos Hub?",
    "Explain IBC protocol",
    "What are zkEVMs?",
]


def ask_question_only(driver, profile_index):
    """
    Just ask a question without selecting mode (used for repeated instant questions)
    Click textarea → click hottest question → press Enter
    """
    try:
        print(f"[Profile {profile_index}] Looking for textarea...")
        time.sleep(1)
        
        # Find textarea by ID
        textarea = None
        try:
            textarea = driver.find_element(By.ID, "chat-input")
            print(f"[Profile {profile_index}] Found textarea by ID")
        except:
            try:
                textarea = driver.find_element(By.XPATH, "//textarea[@id='chat-input']")
            except:
                textarea = driver.find_element(By.XPATH, "//form//textarea")
        
        if not textarea:
            print(f"[Profile {profile_index}] ⚠️ Textarea not found")
            return False
        
        # Click textarea to show suggestions
        print(f"[Profile {profile_index}] Clicking textarea to show suggestions...")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", textarea)
        time.sleep(0.3)
        
        actions = ActionChains(driver)
        actions.move_to_element(textarea).click().perform()
        time.sleep(2)
        
        # Try to click hottest question
        try:
            print(f"[Profile {profile_index}] Searching for hottest questions...")
            time.sleep(1.5)
            
            # Find clickable hottest question elements (buttons or divs with cursor-pointer)
            # Avoid sidebar by looking for elements in the main chat area
            question_rows = []
            
            # Strategy 1: Find button elements containing "Hottest Question" text
            try:
                buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Hottest Question')]")
                for btn in buttons:
                    if btn.is_displayed() and 'sidebar' not in btn.get_attribute('class').lower():
                        question_rows.append(btn)
                print(f"[Profile {profile_index}] Found {len(question_rows)} hottest question buttons")
            except:
                pass
            
            # Strategy 2: Find div with cursor-pointer containing hottest question
            if len(question_rows) == 0:
                try:
                    divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'cursor-pointer') and contains(., 'Hottest Question')]")
                    for div in divs:
                        if div.is_displayed():
                            question_rows.append(div)
                    print(f"[Profile {profile_index}] Found {len(question_rows)} hottest question divs")
                except:
                    pass
            
            # Strategy 3: Find any clickable element (not in sidebar) with hottest question
            if len(question_rows) == 0:
                try:
                    hottest_texts = driver.find_elements(By.XPATH, "//*[contains(text(), 'Hottest Question')]")
                    for elem in hottest_texts:
                        try:
                            # Get the closest clickable parent (button or div with cursor-pointer)
                            clickable = elem.find_element(By.XPATH, "./ancestor::*[self::button or contains(@class, 'cursor-pointer')][1]")
                            if clickable.is_displayed():
                                # Check it's not in sidebar
                                elem_text = clickable.text
                                if 'Toggle Sidebar' not in elem_text and 'New Chat' not in elem_text[:20]:
                                    question_rows.append(clickable)
                        except:
                            pass
                    print(f"[Profile {profile_index}] Found {len(question_rows)} clickable hottest questions")
                except:
                    pass
            
            if len(hottest_elements) > 0:
                # Get visible question rows
                question_rows = []
                for elem in hottest_elements:
                    try:
                        parent = elem.find_element(By.XPATH, "./ancestor::div[contains(@class, 'flex')]")
                        if parent.is_displayed():
                            question_rows.append(parent)
                    except:
                        pass
                
                print(f"[Profile {profile_index}] Found {len(question_rows)} visible question rows")
                
                if len(question_rows) > 0:
                    # Random select one
                    import random as rand
                    selected_row = rand.choice(question_rows)
                    question_text = selected_row.text[:100] if selected_row.text else "(no text)"
                    print(f"[Profile {profile_index}] Selected: {question_text}")
                    
                    # Scroll and hover
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selected_row)
                    time.sleep(0.3)
                    
                    print(f"[Profile {profile_index}] Hovering...")
                    actions = ActionChains(driver)
                    actions.move_to_element(selected_row).pause(0.5).perform()
                    time.sleep(0.5)
                    
                    # Click
                    print(f"[Profile {profile_index}] Clicking...")
                    try:
                        actions = ActionChains(driver)
                        actions.move_to_element(selected_row).click().perform()
                        print(f"[Profile {profile_index}] ✅ Clicked")
                    except:
                        driver.execute_script("arguments[0].click();", selected_row)
                        print(f"[Profile {profile_index}] ✅ Clicked with JS")
                    
                    time.sleep(1.5)
                    
                    # Press Enter
                    print(f"[Profile {profile_index}] Pressing Enter...")
                    textarea = driver.find_element(By.ID, "chat-input")
                    textarea.send_keys(Keys.RETURN)
                    time.sleep(2)
                    print(f"[Profile {profile_index}] ✅ Question submitted!")
                    return True
            
            print(f"[Profile {profile_index}] No questions found, typing manually...")
            random_question = random.choice(SUGGESTED_QUESTIONS)
            textarea.clear()
            textarea.send_keys(random_question)
            time.sleep(0.5)
            textarea.send_keys(Keys.RETURN)
            time.sleep(2)
            print(f"[Profile {profile_index}] ✅ Question submitted!")
            return True
                
        except Exception as e:
            print(f"[Profile {profile_index}] Error with suggestions: {e}, typing manually...")
            random_question = random.choice(SUGGESTED_QUESTIONS)
            textarea.clear()
            textarea.send_keys(random_question)
            time.sleep(0.5)
            textarea.send_keys(Keys.RETURN)
            time.sleep(2)
            print(f"[Profile {profile_index}] ✅ Question submitted!")
            return True
            
    except Exception as e:
        print(f"[Profile {profile_index}] ❌ Error: {str(e)}")
        return False


def select_mode_and_ask(driver, profile_index, mode="deep research"):
    """
    Select mode (deep research or instant) and ask a question
    Args:
        driver: Selenium driver
        profile_index: Profile index for logging
        mode: "deep research" or "instant"
    Returns:
        bool: Success status
    """
    try:
        # Step 1: Find and click button to open chat mode dropdown
        print(f"[Profile {profile_index}] Opening chat mode dropdown...")
        time.sleep(2)
        
        # Debug: Print all buttons on page
        try:
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"[Profile {profile_index}] DEBUG: Found {len(all_buttons)} buttons on page")
            for idx, btn in enumerate(all_buttons[:10]):  # First 10 buttons
                btn_text = btn.text[:50] if btn.text else "(no text)"
                btn_class = btn.get_attribute("class")[:50] if btn.get_attribute("class") else "(no class)"
                print(f"  Button {idx}: {btn_text} | class: {btn_class}")
        except Exception as e:
            print(f"[Profile {profile_index}] DEBUG: Error listing buttons: {e}")
        
        # Try to find dropdown button with multiple strategies
        dropdown_button = None
        
        # Strategy 1: Find button with SVG chevron-down
        try:
            dropdown_button = driver.find_element(By.XPATH, "//button[.//svg[contains(@class, 'chevron-down')]]")
            print(f"[Profile {profile_index}] Found dropdown via chevron-down SVG")
        except:
            pass
        
        # Strategy 2: Find button near textarea in form
        if not dropdown_button:
            try:
                dropdown_button = driver.find_element(By.XPATH, "//form//button[@data-state]")
                print(f"[Profile {profile_index}] Found dropdown via data-state attribute")
            except:
                pass
        
        # Strategy 3: Find any button with aria-haspopup
        if not dropdown_button:
            try:
                dropdown_button = driver.find_element(By.XPATH, "//button[@aria-haspopup='menu']")
                print(f"[Profile {profile_index}] Found dropdown via aria-haspopup")
            except:
                pass
        
        # Strategy 4: Absolute XPath from form
        if not dropdown_button:
            try:
                dropdown_button = driver.find_element(By.XPATH, "/html/body/div[6]/div/main/main/div/div/div/div[2]/form/div[3]/button")
                print(f"[Profile {profile_index}] Found dropdown via absolute XPath")
            except:
                pass
        
        if not dropdown_button:
            print(f"[Profile {profile_index}] ⚠️ Dropdown button not found")
            return False
        
        print(f"[Profile {profile_index}] Found dropdown button: class='{dropdown_button.get_attribute('class')}'")
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_button)
        time.sleep(0.5)
        
        # Try clicking with ActionChains first
        try:
            actions = ActionChains(driver)
            actions.move_to_element(dropdown_button).click().perform()
            print(f"[Profile {profile_index}] Clicked dropdown with ActionChains")
        except Exception as e:
            print(f"[Profile {profile_index}] ActionChains click failed: {e}")
            # Fallback to JavaScript click
            try:
                driver.execute_script("arguments[0].click();", dropdown_button)
                print(f"[Profile {profile_index}] Clicked dropdown with JavaScript")
            except Exception as e2:
                print(f"[Profile {profile_index}] JavaScript click failed: {e2}")
                return False
        
        time.sleep(2)
        
        # Wait for dropdown menu to appear
        print(f"[Profile {profile_index}] Waiting for dropdown menu...")
        menu_appeared = False
        
        for attempt in range(15):  # Try for 7.5 seconds
            try:
                # Look for visible menu
                menus = driver.find_elements(By.XPATH, "//div[@role='menu']")
                print(f"[Profile {profile_index}] Found {len(menus)} menu elements")
                
                for menu in menus:
                    is_displayed = menu.is_displayed()
                    is_hidden = menu.get_attribute("hidden")
                    print(f"[Profile {profile_index}]   Menu: displayed={is_displayed}, hidden={is_hidden}")
                    
                    if is_displayed and not is_hidden:
                        menu_appeared = True
                        print(f"[Profile {profile_index}] ✅ Dropdown menu is visible!")
                        break
                
                if menu_appeared:
                    break
                    
                time.sleep(0.5)
            except Exception as e:
                print(f"[Profile {profile_index}] Menu check error: {e}")
                time.sleep(0.5)
        
        if not menu_appeared:
            print(f"[Profile {profile_index}] ⚠️ Menu did not appear, but continuing...")
        
        time.sleep(1)
        
        # Step 3: Select mode from dropdown menu
        print(f"[Profile {profile_index}] Selecting '{mode}' mode...")
        
        # Debug: List all menuitems
        try:
            all_menuitems = driver.find_elements(By.XPATH, "//div[@role='menuitem']")
            print(f"[Profile {profile_index}] DEBUG: Found {len(all_menuitems)} menu items")
            for idx, item in enumerate(all_menuitems):
                item_text = item.text[:50] if item.text else "(no text)"
                is_visible = item.is_displayed()
                print(f"  MenuItem {idx}: '{item_text}' | visible={is_visible}")
        except Exception as e:
            print(f"[Profile {profile_index}] DEBUG: Error listing menuitems: {e}")
        
        # Find mode element with simpler selectors
        mode_element = None
        target_text = "Deep Research" if "deep" in mode.lower() else "Instant"
        
        # Strategy 1: Direct menuitem with text
        try:
            mode_element = driver.find_element(By.XPATH, f"//div[@role='menuitem' and contains(., '{target_text}')]")
            print(f"[Profile {profile_index}] Found mode via direct menuitem text")
        except:
            pass
        
        # Strategy 2: Find by position
        if not mode_element:
            try:
                position = 3 if "deep" in mode.lower() else 2
                mode_element = driver.find_element(By.XPATH, f"(//div[@role='menuitem'])[{position}]")
                print(f"[Profile {profile_index}] Found mode via position [{position}]")
            except:
                pass
        
        # Strategy 3: Find text div then get parent
        if not mode_element:
            try:
                text_div = driver.find_element(By.XPATH, f"//div[text()='{target_text}']")
                mode_element = text_div.find_element(By.XPATH, "./ancestor::div[@role='menuitem']")
                print(f"[Profile {profile_index}] Found mode via text then ancestor")
            except:
                pass
        
        if not mode_element:
            print(f"[Profile {profile_index}] ⚠️ Mode '{mode}' not found")
            return False
        
        print(f"[Profile {profile_index}] Found '{mode}' option, attempting click...")
        
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mode_element)
        time.sleep(0.3)
        
        # Try ActionChains first
        try:
            actions = ActionChains(driver)
            actions.move_to_element(mode_element).click().perform()
            print(f"[Profile {profile_index}] Clicked mode with ActionChains")
        except Exception as e:
            print(f"[Profile {profile_index}] ActionChains failed: {e}, trying JavaScript...")
            try:
                driver.execute_script("arguments[0].click();", mode_element)
                print(f"[Profile {profile_index}] Clicked mode with JavaScript")
            except Exception as e2:
                print(f"[Profile {profile_index}] ⚠️ All click methods failed: {e2}")
                return False
        
        time.sleep(2)
        print(f"[Profile {profile_index}] ✅ Mode '{mode}' selected")
        
        # Wait for dropdown to close
        time.sleep(1)
        
        # If deep research mode, reload page before asking question
        if "deep" in mode.lower():
            print(f"[Profile {profile_index}] Reloading page after selecting Deep Research mode...")
            driver.refresh()
            time.sleep(10)  # Wait for page to reload
            print(f"[Profile {profile_index}] ✅ Page reloaded")
        
        # Step 3: Click on textarea to show hottest questions
        print(f"[Profile {profile_index}] Clicking textarea to show hottest questions...")
        time.sleep(1)
        
        try:
            # Find textarea by ID
            textarea = driver.find_element(By.ID, "chat-input")
            
            # Scroll into view and click
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", textarea)
            time.sleep(0.5)
            
            # Click to focus and show suggestions
            actions = ActionChains(driver)
            actions.move_to_element(textarea).click().perform()
            print(f"[Profile {profile_index}] Clicked textarea, waiting for suggestions...")
            time.sleep(2)
            
            # Debug: Look for hottest questions
            try:
                print(f"[Profile {profile_index}] DEBUG: Searching for hottest questions...")
                time.sleep(1.5)  # Wait a bit more for list to appear
                
                # Find clickable hottest question elements (not sidebar)
                question_rows = []
                
                # Strategy 1: Find button elements containing "Hottest Question" text
                try:
                    buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Hottest Question')]")
                    for btn in buttons:
                        if btn.is_displayed() and 'sidebar' not in btn.get_attribute('class').lower():
                            question_rows.append(btn)
                    print(f"[Profile {profile_index}] Found {len(question_rows)} hottest question buttons")
                except:
                    pass
                
                # Strategy 2: Find div with cursor-pointer
                if len(question_rows) == 0:
                    try:
                        divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'cursor-pointer') and contains(., 'Hottest Question')]")
                        for div in divs:
                            if div.is_displayed():
                                question_rows.append(div)
                        print(f"[Profile {profile_index}] Found {len(question_rows)} hottest question divs")
                    except:
                        pass
                
                # Strategy 3: Find clickable parent (not sidebar)
                if len(question_rows) == 0:
                    try:
                        hottest_texts = driver.find_elements(By.XPATH, "//*[contains(text(), 'Hottest Question')]")
                        for elem in hottest_texts:
                            try:
                                clickable = elem.find_element(By.XPATH, "./ancestor::*[self::button or contains(@class, 'cursor-pointer')][1]")
                                if clickable.is_displayed():
                                    elem_text = clickable.text
                                    if 'Toggle Sidebar' not in elem_text and 'New Chat' not in elem_text[:20]:
                                        question_rows.append(clickable)
                            except:
                                pass
                        print(f"[Profile {profile_index}] Found {len(question_rows)} clickable elements")
                    except:
                        pass
                
                if len(hottest_elements) > 0:
                    # Get all visible hottest question rows
                    question_rows = []
                    for elem in hottest_elements:
                        try:
                            # Get the parent container of hottest question
                            parent = elem.find_element(By.XPATH, "./ancestor::div[contains(@class, 'flex')]")
                            if parent.is_displayed():
                                question_rows.append(parent)
                        except:
                            pass
                    
                    print(f"[Profile {profile_index}] DEBUG: Found {len(question_rows)} visible question rows")
                    
                    if len(question_rows) > 0:
                        # Random select one question
                        import random as rand
                        selected_row = rand.choice(question_rows)
                        question_text = selected_row.text[:100] if selected_row.text else "(no text)"
                        print(f"[Profile {profile_index}] Selected question: {question_text}")
                        
                        # Scroll into view
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selected_row)
                        time.sleep(0.3)
                        
                        # Hover to the element first
                        print(f"[Profile {profile_index}] Hovering to question...")
                        actions = ActionChains(driver)
                        actions.move_to_element(selected_row).pause(0.5).perform()
                        time.sleep(0.5)
                        
                        # Now click (try left click first, then right click if needed)
                        print(f"[Profile {profile_index}] Clicking question...")
                        try:
                            actions = ActionChains(driver)
                            actions.move_to_element(selected_row).click().perform()
                            print(f"[Profile {profile_index}] ✅ Clicked with left click")
                        except:
                            try:
                                actions = ActionChains(driver)
                                actions.move_to_element(selected_row).context_click().perform()
                                print(f"[Profile {profile_index}] ✅ Clicked with right click")
                            except:
                                # Fallback to JavaScript
                                driver.execute_script("arguments[0].click();", selected_row)
                                print(f"[Profile {profile_index}] ✅ Clicked with JavaScript")
                        
                        time.sleep(1.5)
                        
                        # Press Enter to submit
                        print(f"[Profile {profile_index}] Pressing Enter to submit...")
                        textarea = driver.find_element(By.ID, "chat-input")
                        textarea.send_keys(Keys.RETURN)
                        time.sleep(2)
                        print(f"[Profile {profile_index}] ✅ Question submitted with Enter key!")
                        return True
                
                print(f"[Profile {profile_index}] ⚠️ No question rows found, typing manually...")
                # Fallback to typing
                random_question = random.choice(SUGGESTED_QUESTIONS)
                textarea.clear()
                textarea.send_keys(random_question)
                print(f"[Profile {profile_index}] Question: {random_question}")
                time.sleep(0.5)
                textarea.send_keys(Keys.RETURN)
                time.sleep(2)
                print(f"[Profile {profile_index}] ✅ Question submitted!")
                return True
                    
            except Exception as e:
                print(f"[Profile {profile_index}] DEBUG: Error finding questions: {e}")
                # Fallback to typing
                random_question = random.choice(SUGGESTED_QUESTIONS)
                textarea.clear()
                textarea.send_keys(random_question)
                print(f"[Profile {profile_index}] Question: {random_question}")
                time.sleep(0.5)
                textarea.send_keys(Keys.RETURN)
                time.sleep(2)
                print(f"[Profile {profile_index}] ✅ Question submitted!")
                return True
                
        except Exception as e:
            print(f"[Profile {profile_index}] ⚠️ Cannot interact with textarea: {e}")
            return False
            
    except Exception as e:
        print(f"[Profile {profile_index}] ❌ Error in select_mode_and_ask: {str(e)}")
        return False


def asksurf_automation(profile_path, profile_index):
    """
    AskSurf automation for one profile
    Args:
        profile_path: Path to Firefox profile
        profile_index: Profile index for logging
    """
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"[Profile {profile_index}] Starting AskSurf automation")
        print(f"{'='*60}\n")
        
        # Create driver
        driver = create_firefox_driver(profile_path, optimize=True)
        
        # Step 1: Access website
        print(f"[Profile {profile_index}] Accessing {ASKSURF_URL}")
        driver.get(ASKSURF_URL)
        time.sleep(WAIT_PAGE_LOAD)
        
        # Step 2: Login process
        print(f"[Profile {profile_index}] Starting login process...")
        
        # Find and click "Log in or sign up" button
        login_selectors = [
            "//button[contains(text(), 'Log in')]",
            "//button[contains(text(), 'sign up')]",
            "//a[contains(text(), 'Log in')]",
            "//a[contains(text(), 'sign up')]",
            "//*[contains(text(), 'Log in or sign up')]",
        ]
        
        login_button = find_element_by_selectors(driver, login_selectors, ELEMENT_TIMEOUT)
        if not login_button:
            print(f"[Profile {profile_index}] ⚠️ Login button not found")
            return False
            
        print(f"[Profile {profile_index}] Found login button, clicking...")
        click_element_safe(driver, login_button)
        time.sleep(WAIT_AFTER_LOGIN)
        
        # Save main window handle
        main_window = driver.current_window_handle
        print(f"[Profile {profile_index}] Main window saved")
        
        # Click Google login button (will open new window/tab)
        print(f"[Profile {profile_index}] Looking for Google login button...")
        google_selectors = [
            "//button[contains(., 'Continue with Google')]",
            "//button[contains(., 'Google')]",
            "//button[contains(., 'Sign in with Google')]",
            "//*[contains(@class, 'google')]//button",
            "//button[.//text()[contains(., 'Google')]]",
        ]
        
        google_button = find_element_by_selectors(driver, google_selectors, ELEMENT_TIMEOUT)
        if not google_button:
            print(f"[Profile {profile_index}] ⚠️ Google button not found")
            return False
        
        print(f"[Profile {profile_index}] Found Google button, clicking...")
        click_element_safe(driver, google_button)
        time.sleep(3)
        
        # Switch to new window (Google login popup)
        print(f"[Profile {profile_index}] Switching to Google login window...")
        all_windows = driver.window_handles
        for window in all_windows:
            if window != main_window:
                driver.switch_to.window(window)
                print(f"[Profile {profile_index}] Switched to Google login window")
                break
        
        # Select Google account in popup window
        print(f"[Profile {profile_index}] Looking for Google account selection...")
        time.sleep(3)
        
        account_selectors = [
            "//li[1]//div[@role='link']",
            "//div[@data-authuser='0']",
            "//ul//li[1]//div[contains(@class, 'BHzsHc')]",
            "(//div[contains(@jsname, 'V67aGc')])[1]",
            "//div[@role='link']",
        ]
        
        google_account = find_element_by_selectors(driver, account_selectors, 10)
        if google_account:
            print(f"[Profile {profile_index}] Found Google account, selecting...")
            click_element_safe(driver, google_account)
            time.sleep(WAIT_ACCOUNT_SELECT)
        else:
            print(f"[Profile {profile_index}] No account selection needed (maybe already logged in)")
        
        # Click continue if present
        continue_selectors = [
            "//button[contains(., 'Continue')]",
            "//button[contains(., 'Tiếp tục')]",
        ]
        continue_button = find_element_by_selectors(driver, continue_selectors, 5)
        if continue_button:
            print(f"[Profile {profile_index}] Found continue button, clicking...")
            click_element_safe(driver, continue_button)
            time.sleep(2)
        
        # Wait for popup to close or redirect
        print(f"[Profile {profile_index}] Waiting for login to complete...")
        time.sleep(WAIT_GOOGLE_LOGIN)
        
        # Switch back to main window
        print(f"[Profile {profile_index}] Switching back to main window...")
        driver.switch_to.window(main_window)
        print(f"[Profile {profile_index}] ✅ Login completed, back to main window")
        
        # Wait for main page to reload after login
        print(f"[Profile {profile_index}] Waiting for page to reload after login...")
        time.sleep(5)
        
        # Verify chat interface is ready
        print(f"[Profile {profile_index}] Verifying chat interface...")
        chat_indicators = [
            "//textarea[@id='chat-input']",
            "//textarea[@placeholder]",
            "//button[contains(., 'Auto')]",
        ]
        if find_element_by_selectors(driver, chat_indicators, 10):
            print(f"[Profile {profile_index}] ✅ Chat interface loaded successfully")
        else:
            print(f"[Profile {profile_index}] ⚠️ Chat interface not found, but continuing...")
        
        # Step 2: Instant mode (10 times, wait 15 seconds each)
        print(f"\n[Profile {profile_index}] === STEP 2: Instant Mode (x{INSTANT_REPEAT_COUNT}) ===")
        
        # First instant question with mode selection
        print(f"\n[Profile {profile_index}] --- Instant Question 1/{INSTANT_REPEAT_COUNT} ---")
        if select_mode_and_ask(driver, profile_index, mode="instant"):
            print(f"[Profile {profile_index}] Waiting {WAIT_BETWEEN_INSTANT} seconds...")
            time.sleep(WAIT_BETWEEN_INSTANT)
            
            # Remaining 9 instant questions - Click "New Chat" then ask (mode already set to instant)
            for i in range(2, INSTANT_REPEAT_COUNT + 1):
                print(f"\n[Profile {profile_index}] --- Instant Question {i}/{INSTANT_REPEAT_COUNT} ---")
                
                # Click "New chat" to start new conversation (instant mode is retained)
                print(f"[Profile {profile_index}] Looking for 'New chat' button...")
                new_chat_selectors = [
                    "//button[@data-sidebar='menu-button']//span[contains(text(), 'New Chat')]",
                    "//button[contains(@class, 'peer/menu-button')]//span[contains(text(), 'New Chat')]",
                    "//button//span[contains(text(), 'New Chat')]",
                    "//button//span[text()='New Chat']",
                    "//*[contains(text(), 'New Chat')]",
                ]
                
                new_chat_button = find_element_by_selectors(driver, new_chat_selectors, 10)
                if new_chat_button:
                    print(f"[Profile {profile_index}] Found 'New chat' button, clicking...")
                    click_element_safe(driver, new_chat_button)
                    time.sleep(3)
                    print(f"[Profile {profile_index}] ✅ New chat opened")
                else:
                    print(f"[Profile {profile_index}] ⚠️ New chat button not found, continuing anyway...")
                
                # Ask question without selecting mode (instant mode is already active)
                if ask_question_only(driver, profile_index):
                    print(f"[Profile {profile_index}] Waiting {WAIT_BETWEEN_INSTANT} seconds...")
                    time.sleep(WAIT_BETWEEN_INSTANT)
                else:
                    print(f"[Profile {profile_index}] ⚠️ Instant question {i} failed, skipping...")
                    time.sleep(3)
        else:
            print(f"[Profile {profile_index}] ⚠️ First instant question failed!")
        
        # Step 3: Deep Research mode (1 time, wait 2 minutes)
        print(f"\n[Profile {profile_index}] === STEP 3: Deep Research Mode ===")
        
        # Click "New Chat" button before deep research
        print(f"[Profile {profile_index}] Looking for 'New Chat' button before deep research...")
        new_chat_selectors = [
            "//button[@data-sidebar='menu-button']//span[contains(text(), 'New Chat')]",
            "//button[contains(@class, 'peer/menu-button')]//span[contains(text(), 'New Chat')]",
            "//button//span[contains(text(), 'New Chat')]",
            "//button//span[text()='New Chat']",
            "//*[contains(text(), 'New Chat')]",
        ]
        
        new_chat_button = find_element_by_selectors(driver, new_chat_selectors, 10)
        if new_chat_button:
            print(f"[Profile {profile_index}] Found 'New Chat' button, clicking...")
            click_element_safe(driver, new_chat_button)
            time.sleep(3)
            print(f"[Profile {profile_index}] ✅ Clicked 'New Chat' button")
        else:
            print(f"[Profile {profile_index}] ⚠️ 'New Chat' button not found, continuing anyway...")
        
        if select_mode_and_ask(driver, profile_index, mode="deep research"):
            print(f"[Profile {profile_index}] Waiting {WAIT_AFTER_DEEP_RESEARCH} seconds (2 minutes) for deep research response...")
            time.sleep(WAIT_AFTER_DEEP_RESEARCH)
        else:
            print(f"[Profile {profile_index}] ⚠️ Deep research failed!")
        
        # Final wait before closing
        print(f"\n[Profile {profile_index}] All questions completed! Waiting before closing...")
        time.sleep(WAIT_BEFORE_CLOSE)
        
        print(f"[Profile {profile_index}] ✅ Automation completed successfully")
        return True
        
    except Exception as e:
        print(f"[Profile {profile_index}] ❌ Error: {str(e)}")
        return False
        
    finally:
        if driver:
            print(f"[Profile {profile_index}] Closing browser...")
            try:
                driver.quit()
            except:
                pass
        cleanup_all(profile_path, profile_index)


def run_single_profile(profile_index=1):
    """Run automation for a single profile"""
    if profile_index < 1 or profile_index > len(FIREFOX_PROFILES):
        print(f"❌ Invalid profile index. Use 1-{len(FIREFOX_PROFILES)}")
        return
    
    profile_path = FIREFOX_PROFILES[profile_index - 1]
    asksurf_automation(profile_path, profile_index)


def run_all_profiles():
    """Run automation for all profiles in batches"""
    print("\n" + "="*60)
    print("ASKSURF.AI AUTOMATION - ALL PROFILES")
    print("="*60 + "\n")
    
    run_all_batches(
        task_function=asksurf_automation,
        profiles=FIREFOX_PROFILES,
        wait_between_batches=WAIT_BETWEEN_BATCHES
    )
    
    print("\n" + "="*60)
    print("ALL PROFILES COMPLETED!")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_profiles()

