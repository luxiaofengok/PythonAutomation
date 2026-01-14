from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

"""
ActionChains Usage Demo - Menu Hover Example

This script demonstrates how to use ActionChains for hovering over menu items.

WHY USE ActionChains?
- Cannot hover with element.click() - hovering requires ActionChains
- Simulates real mouse movements
- Essential for dropdown menus that appear only on hover

HOW IT DIFFERS FROM REGULAR METHODS:
- element.click() -> Direct click, no hover capability
- ActionChains.move_to_element() -> Can hover to reveal hidden menus
- Must call .perform() to execute the action
"""


def demo_menu_hover():
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.get("https://demoqa.com/menu#")
        wait = WebDriverWait(driver, 10)

        # try click 'Elements' button if present (fallbacks included)
        try:
            el_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Elements']")))
            el_btn.click()
            # if navigation happens, return to menu page
            if 'elements' in driver.current_url.lower():
                driver.get("https://demoqa.com/menu#")
        except Exception:
            pass

        # HOVER EXAMPLE: Using ActionChains to reveal dropdown menu
        # Why ActionChains? Regular click() cannot hover - it only clicks
        # move_to_element() simulates mouse hovering, revealing hidden submenus
        main_item = wait.until(EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Main Item 2']")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", main_item)
        
        # ActionChains.move_to_element() performs HOVER action (not click)
        # .perform() is required to execute the action chain
        ActionChains(driver).move_to_element(main_item).perform()

        # Wait for submenu to become visible after hovering over main item
        # Then hover over the sub item using ActionChains again
        sub_item_xpath = "//li[a[normalize-space()='Main Item 2']]//a[normalize-space()='Sub Item']"
        try:
            sub_item = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, sub_item_xpath)))
            # Another hover action to interact with nested menu
            ActionChains(driver).move_to_element(sub_item).perform()
        except Exception:
            # Fallback: try a looser search if exact submenu not found
            try:
                sub_item = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(normalize-space(),'Sub Item')]") ))
                ActionChains(driver).move_to_element(sub_item).perform()
            except Exception:
                raise RuntimeError('Sub Item not found')

    finally:
        driver.quit()


if __name__ == '__main__':
    demo_menu_hover()


def test_move_hover():
    """Pytest wrapper so the script is collected as a test."""
    demo_menu_hover()