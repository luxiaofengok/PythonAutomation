from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from time import sleep


def demo_menu_hover():
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.get("https://demoqa.com/menu#")
        wait = WebDriverWait(driver, 10)

        # hover Main Item 2 then Sub Item
        main_item = wait.until(EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Main Item 2']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", main_item)
        ActionChains(driver).move_to_element(main_item).perform()
        sleep(5)  # Wait 5 seconds after hovering

        # wait for its submenu items to appear, then hover 'Sub Item'
        sub_item_xpath = "//li[a[normalize-space()='Main Item 2']]//a[normalize-space()='Sub Item']"
        try:
            sub_item = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, sub_item_xpath)))
            ActionChains(driver).move_to_element(sub_item).perform()
            sleep(5)  # Wait 5 seconds after hovering
            
            # Now hover to Sub Sub List
            sub_sub_list_xpath = "//a[normalize-space()='SUB SUB LIST »']"
            try:
                sub_sub_list = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, sub_sub_list_xpath)))
                ActionChains(driver).move_to_element(sub_sub_list).perform()
                print("✓ Hovering on Sub Sub List")
                sleep(5)  # Wait 5 seconds after hovering
                
                # Hover on one of the sub sub list items (e.g., "Sub Sub Item 1")
                try:
                    sub_sub_item1 = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Sub Sub Item 1']")))
                    ActionChains(driver).move_to_element(sub_sub_item1).perform()
                    print("✓ Hovering on Sub Sub Item 1")
                    sleep(5)  # Wait 5 seconds on the actual item
                except Exception as e:
                    print(f"⚠️ Sub Sub Item 1 not found: {e}")
                    
            except Exception as e:
                print(f"⚠️ Sub Sub List not found: {e}")
                
        except Exception:
            # if direct sub-item not found, try a looser search
            try:
                sub_item = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(normalize-space(),'Sub Item')]") ))
                ActionChains(driver).move_to_element(sub_item).perform()
                sleep(5)  # Wait 5 seconds after hovering
                
                # Try to find Sub Sub List
                try:
                    sub_sub_list = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(normalize-space(),'SUB SUB')]")))
                    ActionChains(driver).move_to_element(sub_sub_list).perform()
                    print("✓ Hovering on Sub Sub List")
                    sleep(5)  # Wait 5 seconds after hovering
                    
                    # Hover on one of the sub sub list items
                    try:
                        sub_sub_item1 = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(normalize-space(),'Sub Sub Item 1')]")))
                        ActionChains(driver).move_to_element(sub_sub_item1).perform()
                        print("✓ Hovering on Sub Sub Item 1")
                        sleep(5)  # Wait 5 seconds on the actual item
                    except Exception as e:
                        print(f"⚠️ Sub Sub Item 1 not found: {e}")
                        
                except Exception as e:
                    print(f"⚠️ Sub Sub List not found: {e}")
                    
            except Exception:
                raise RuntimeError('Sub Item not found')

    finally:
        driver.quit()


if __name__ == '__main__':
    demo_menu_hover()


def test_move_hover():
    """Pytest wrapper so the script is collected as a test."""
    demo_menu_hover()