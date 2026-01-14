# ActionChains trong Selenium - Hướng dẫn sử dụng

## ActionChains là gì? (What is ActionChains?)

`ActionChains` là một class trong Selenium WebDriver được sử dụng để thực hiện các thao tác phức tạp với chuột và bàn phím. Nó cho phép bạn tạo ra một chuỗi các hành động và thực thi chúng một cách tuần tự.

## Khi nào nên sử dụng ActionChains? (When to use ActionChains?)

Sử dụng `ActionChains` khi bạn cần:

1. **Di chuyển chuột (Hover)**: Di chuyển chuột đến một phần tử để hiển thị menu hoặc tooltip
2. **Kéo và thả (Drag and Drop)**: Kéo một phần tử và thả vào vị trí khác
3. **Click phải (Right Click/Context Click)**: Thực hiện click chuột phải
4. **Double Click**: Click đúp vào phần tử
5. **Nhấn giữ phím (Key Press)**: Nhấn và giữ các phím như Ctrl, Shift
6. **Chuỗi hành động phức tạp**: Kết hợp nhiều hành động liên tiếp

## Sự khác biệt giữa ActionChains và các phương thức thông thường

### 1. Click thông thường vs ActionChains click

**Click thông thường:**
```python
element.click()  # Click trực tiếp vào phần tử
```

**ActionChains click:**
```python
ActionChains(driver).click(element).perform()  # Click sử dụng ActionChains
```

**Khác biệt:**
- Click thông thường: Nhanh, đơn giản, phù hợp cho hầu hết trường hợp
- ActionChains click: Mô phỏng hành động chuột thực tế, cần thiết khi JavaScript theo dõi sự kiện chuột

### 2. Hover (move_to_element) - Tính năng độc quyền của ActionChains

**Không thể làm với click thông thường:**
```python
ActionChains(driver).move_to_element(menu_item).perform()
```

**Ứng dụng:**
- Hiển thị menu dropdown khi hover
- Hiển thị tooltip
- Kích hoạt các hiệu ứng CSS :hover

### 3. Drag and Drop

**Sử dụng ActionChains:**
```python
ActionChains(driver).drag_and_drop(source, target).perform()
# Hoặc
ActionChains(driver).click_and_hold(source).move_to_element(target).release().perform()
```

**Không thể thực hiện bằng phương thức thông thường**

### 4. Click phải (Context Click)

**ActionChains:**
```python
ActionChains(driver).context_click(element).perform()
```

**Không có phương thức tương đương trong element thông thường**

## Ví dụ thực tế

### Ví dụ 1: Hover để hiển thị menu (Từ test_movehover.py)

```python
from selenium.webdriver import ActionChains

# Di chuyển chuột đến menu chính
main_item = driver.find_element(By.XPATH, "//a[normalize-space()='Main Item 2']")
ActionChains(driver).move_to_element(main_item).perform()

# Sau đó di chuyển đến submenu
sub_item = driver.find_element(By.XPATH, "//a[normalize-space()='Sub Item']")
ActionChains(driver).move_to_element(sub_item).perform()
```

### Ví dụ 2: Kéo và thả

```python
source = driver.find_element(By.ID, "draggable")
target = driver.find_element(By.ID, "droppable")

ActionChains(driver).drag_and_drop(source, target).perform()
```

### Ví dụ 3: Double Click

```python
element = driver.find_element(By.ID, "double-click-btn")
ActionChains(driver).double_click(element).perform()
```

### Ví dụ 4: Click phải và chọn option

```python
element = driver.find_element(By.ID, "context-menu-target")
ActionChains(driver).context_click(element).perform()
```

### Ví dụ 5: Chuỗi hành động phức tạp

```python
# Nhấn giữ Ctrl và click nhiều phần tử
from selenium.webdriver.common.keys import Keys

ActionChains(driver)\
    .key_down(Keys.CONTROL)\
    .click(element1)\
    .click(element2)\
    .click(element3)\
    .key_up(Keys.CONTROL)\
    .perform()
```

## Tại sao phải gọi .perform()?

`ActionChains` xây dựng một chuỗi các hành động nhưng **không thực thi ngay lập tức**. Bạn phải gọi `.perform()` để thực thi tất cả các hành động đã được thêm vào chuỗi.

```python
# Sai - không thực thi
ActionChains(driver).move_to_element(element)

# Đúng - thực thi hành động
ActionChains(driver).move_to_element(element).perform()
```

## So sánh tổng quan

| Tính năng | Phương thức thông thường | ActionChains |
|-----------|-------------------------|--------------|
| Click đơn giản | ✅ `element.click()` | ✅ `ActionChains.click()` |
| Nhập text | ✅ `element.send_keys()` | ✅ `ActionChains.send_keys()` |
| Hover | ❌ Không có | ✅ `move_to_element()` |
| Drag & Drop | ❌ Không có | ✅ `drag_and_drop()` |
| Click phải | ❌ Không có | ✅ `context_click()` |
| Double Click | ❌ Không có | ✅ `double_click()` |
| Nhấn giữ phím | ❌ Không có | ✅ `key_down()/key_up()` |
| Độ phức tạp | Đơn giản | Phức tạp hơn |
| Tốc độ | Nhanh | Chậm hơn một chút |
| Mô phỏng người dùng | Cơ bản | Chân thực hơn |

## Kết luận

- **Sử dụng phương thức thông thường** (click, send_keys) cho các thao tác đơn giản để code ngắn gọn và nhanh hơn
- **Sử dụng ActionChains** khi cần:
  - Hover để hiển thị menu/tooltip
  - Kéo và thả
  - Click phải, double click
  - Mô phỏng hành động người dùng phức tạp
  - Kết hợp nhiều hành động chuột/bàn phím

## Các phương thức quan trọng của ActionChains

- `move_to_element(element)` - Di chuyển chuột đến phần tử
- `click(element)` - Click vào phần tử
- `click_and_hold(element)` - Click và giữ chuột
- `release(element)` - Thả chuột
- `context_click(element)` - Click phải
- `double_click(element)` - Click đúp
- `drag_and_drop(source, target)` - Kéo và thả
- `send_keys(keys)` - Gửi phím
- `key_down(key)` - Nhấn giữ phím
- `key_up(key)` - Thả phím
- `pause(seconds)` - Tạm dừng giữa các hành động
- `perform()` - Thực thi chuỗi hành động
