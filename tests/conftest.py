import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def driver():
    # day la phan setup cho cac test script va dung 1 lan duy nhat(before test)
    driver=webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    url="https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    driver.get(url)
    yield driver #cho script chay het roi moi toi teardown(after test)
    
    #day la phan teardown cho moi script
    driver.quit()
    

