# Practice Tests - Selenium Examples

## ActionChains - Cái này dùng để làm gì? Khác gì với click thông thường?

### Trả lời ngắn gọn:
**ActionChains** được dùng để thực hiện các hành động phức tạp với chuột và bàn phím mà các phương thức thông thường như `click()` hay `send_keys()` không làm được.

### Sự khác biệt chính:

#### 1. **Click thông thường** (`element.click()`):
- Click trực tiếp vào phần tử
- Đơn giản, nhanh
- **KHÔNG THỂ** hover (di chuyển chuột để hiển thị menu)

#### 2. **ActionChains** (`ActionChains(driver).move_to_element(element).perform()`):
- Mô phỏng hành động chuột thực tế
- **CÓ THỂ** hover để hiển thị menu ẩn
- **CÓ THỂ** kéo thả, click phải, double click
- Phức tạp hơn, cần gọi `.perform()` để thực thi

## Các Test Scripts trong thư mục này

### 1. test_alert.py
**Mục đích**: Xử lý JavaScript alerts  
**Khác biệt**: Không dùng ActionChains, dùng `switch_to.alert`

```python
# Click button để hiển thị alert
btn.click()  # Dùng click thông thường

# Xử lý alert (không phải ActionChains)
driver.switch_to.alert.accept()
```

### 2. test_form.py
**Mục đích**: Submit form đăng nhập  
**Khác biệt**: Không cần ActionChains, dùng `element.submit()`

```python
# Nhập username và password - dùng phương thức thông thường
username_el.send_keys("tomsmith")
password_el.send_keys("SuperSecretPassword!")

# Submit form - không cần ActionChains
username_el.submit()
```

### 3. test_movehover.py ⭐ (SỬ DỤNG ActionChains)
**Mục đích**: Hover chuột để hiển thị menu dropdown  
**Tại sao cần ActionChains**: `element.click()` KHÔNG THỂ hover

```python
# ❌ KHÔNG THỂ dùng click thông thường cho hover
# element.click()  # Chỉ click, không hover

# ✅ PHẢI dùng ActionChains để hover
ActionChains(driver).move_to_element(main_item).perform()
```

**Giải thích từng bước:**

```python
# Bước 1: Tìm menu chính
main_item = driver.find_element(By.XPATH, "//a[normalize-space()='Main Item 2']")

# Bước 2: Di chuyển chuột đến menu (HOVER) - chỉ ActionChains làm được
ActionChains(driver).move_to_element(main_item).perform()

# Bước 3: Menu con xuất hiện sau khi hover
sub_item = driver.find_element(By.XPATH, "//a[normalize-space()='Sub Item']")

# Bước 4: Hover tiếp vào menu con
ActionChains(driver).move_to_element(sub_item).perform()
```

### 4. test_switch_window.py
**Mục đích**: Chuyển đổi giữa các cửa sổ/tab  
**Khác biệt**: Không dùng ActionChains, dùng `switch_to.window()`

```python
# Click để mở cửa sổ mới - dùng click thông thường
open_btn.click()

# Chuyển sang cửa sổ mới - không phải ActionChains
driver.switch_to.window(new_handle)
```

## Tóm tắt: Khi nào dùng ActionChains?

### ✅ CẦN dùng ActionChains:
1. **Hover** (di chuyển chuột) - `move_to_element()`
2. **Kéo thả** (drag & drop) - `drag_and_drop()`
3. **Click phải** - `context_click()`
4. **Double click** - `double_click()`
5. **Nhấn giữ phím** (Ctrl, Shift) - `key_down()` / `key_up()`
6. **Chuỗi hành động phức tạp**

### ❌ KHÔNG cần ActionChains:
1. Click đơn giản - dùng `element.click()`
2. Nhập text - dùng `element.send_keys()`
3. Submit form - dùng `element.submit()`
4. Chuyển cửa sổ - dùng `driver.switch_to.window()`
5. Xử lý alert - dùng `driver.switch_to.alert`
6. Chọn dropdown - dùng `Select(element).select_by_value()`

## Ví dụ so sánh trực quan

### Scenario 1: Click button thông thường
```python
# Đơn giản - không cần ActionChains
button = driver.find_element(By.ID, "submit-btn")
button.click()  # ✅ Dùng click thông thường
```

### Scenario 2: Hover để hiển thị menu
```python
# Phức tạp - BẮT BUỘC dùng ActionChains
menu = driver.find_element(By.ID, "main-menu")
# menu.click()  # ❌ SAI - click không làm menu xuất hiện

ActionChains(driver).move_to_element(menu).perform()  # ✅ ĐÚNG
```

### Scenario 3: Kéo thả phần tử
```python
# Không thể dùng click - BẮT BUỘC ActionChains
source = driver.find_element(By.ID, "draggable")
target = driver.find_element(By.ID, "droppable")

# Cách 1: Dùng drag_and_drop
ActionChains(driver).drag_and_drop(source, target).perform()

# Cách 2: Dùng chuỗi hành động
ActionChains(driver)\
    .click_and_hold(source)\
    .move_to_element(target)\
    .release()\
    .perform()
```

## Ghi chú quan trọng về .perform()

**Luôn nhớ gọi `.perform()` khi dùng ActionChains!**

```python
# ❌ SAI - không thực thi
ActionChains(driver).move_to_element(element)

# ✅ ĐÚNG - có thực thi
ActionChains(driver).move_to_element(element).perform()
```

## Tài liệu tham khảo

Xem thêm tài liệu chi tiết tại: [docs/ACTION_CHAINS_GUIDE.md](../docs/ACTION_CHAINS_GUIDE.md)
