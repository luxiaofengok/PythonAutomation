import pytest
from selenium import webdriver
from utils.config_reader import ConfigReader

@pytest.fixture(scope="function")
def driver():
    # day la phan setup cho cac test script va dung 1 lan duy nhat(before test)
    # driver=webdriver.Chrome()
    # driver.implicitly_wait(10)
    # driver.maximize_window()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless Chrome
    driver = webdriver.Chrome(options=options)
    url="https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    #url="https://www.letskodeit.com/practice"
    #url=ConfigReader.get_base_url()
    driver.get(url)
    yield driver #cho script chay het roi moi toi teardown(after test)
    
    #day la phan teardown cho moi script
    driver.quit()
    

