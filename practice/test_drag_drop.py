from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from time import sleep


def test_drag_and_drop():
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome()
    driver.implicitly_wait(20)
    driver.maximize_window()
    
    try:
        # Truy cập trang web
        driver.get("https://demoqa.com/droppable")
        sleep(2)  # Dừng 2 giây để theo dõi
        
        # Tìm element "Drag me"
        drag_element = driver.find_element(By.ID, "draggable")
        
        # Cuộn đến element drag_element và đặt ở trung tâm màn hình
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", drag_element)
        sleep(2)  # Dừng 2 giây để theo dõi
        
        # Tìm element "Drop here"
        drop_element = driver.find_element(By.ID, "droppable")
        sleep(2)  # Dừng 2 giây để theo dõi
        
        # Thực hiện hành động kéo và thả
        action = ActionChains(driver)
        action.drag_and_drop(drag_element, drop_element).perform()
        sleep(2)  # Dừng 2 giây để theo dõi kết quả
        
        # Kiểm tra xem đã thả thành công chưa
        drop_text = drop_element.text
        print(f"Kết quả: {drop_text}")
        assert "Dropped!" in drop_text, "Kéo thả không thành công!"
        
        sleep(2)  # Dừng thêm 2 giây để xem kết quả cuối cùng
        
    finally:
        # Đóng trình duyệt
        driver.quit()