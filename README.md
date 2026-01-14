# Python Automation with Selenium

This repository contains Python automation scripts using Selenium WebDriver for testing web applications.

## 📚 Documentation

### ActionChains - What is it and how is it different?

**Question**: *"Cái này dùng để làm gì, khác gì với ask (click)?"*

**Answer**: `ActionChains` is used for complex mouse and keyboard interactions that regular methods like `click()` cannot perform.

**Key Differences:**

| Feature | Regular Method | ActionChains |
|---------|---------------|--------------|
| Simple Click | `element.click()` ✅ | `ActionChains.click()` ✅ |
| Hover | ❌ Not possible | `move_to_element()` ✅ |
| Drag & Drop | ❌ Not possible | `drag_and_drop()` ✅ |
| Right Click | ❌ Not possible | `context_click()` ✅ |
| Double Click | ❌ Not possible | `double_click()` ✅ |

**When to use ActionChains:**
- ✅ Hover over menus to reveal dropdowns
- ✅ Drag and drop elements
- ✅ Right-click, double-click
- ✅ Complex mouse/keyboard sequences

**When NOT to use ActionChains:**
- ❌ Simple clicks → use `element.click()`
- ❌ Typing text → use `element.send_keys()`
- ❌ Form submission → use `element.submit()`

### 📖 Detailed Documentation

- **[ActionChains Complete Guide](docs/ACTION_CHAINS_GUIDE.md)** - Full Vietnamese documentation
- **[Practice Tests README](practice/README.md)** - Examples and comparisons

## 🗂️ Project Structure

```
PythonAutomation/
├── docs/
│   └── ACTION_CHAINS_GUIDE.md    # Comprehensive ActionChains guide
├── pages/
│   ├── base_page.py              # Base page object
│   └── login_page.py             # Login page object
├── practice/
│   ├── README.md                 # Practice examples documentation
│   ├── test_alert.py             # Alert handling (no ActionChains)
│   ├── test_form.py              # Form submission (no ActionChains)
│   ├── test_movehover.py         # Menu hover (USES ActionChains) ⭐
│   └── test_switch_window.py     # Window switching (no ActionChains)
├── tests/
│   ├── conftest.py               # Pytest fixtures
│   ├── test_login.py             # Login tests
│   ├── test_dropdown.py          # Dropdown selection
│   └── test_practice.py          # Practice tests
├── utils/
│   └── config_reader.py          # Configuration reader
├── testsetting.json              # Test configuration
└── pytest.ini                    # Pytest configuration
```

## 🚀 Quick Example: ActionChains vs Regular Click

### Example 1: Simple Click (No ActionChains needed)
```python
# For simple button clicks
button = driver.find_element(By.ID, "submit")
button.click()  # ✅ Use regular click
```

### Example 2: Hover Menu (MUST use ActionChains)
```python
from selenium.webdriver import ActionChains

# Hover to reveal dropdown menu
menu = driver.find_element(By.ID, "main-menu")
ActionChains(driver).move_to_element(menu).perform()  # ✅ ActionChains required

# Regular click CANNOT hover
# menu.click()  # ❌ This won't work for hover!
```

### Example 3: Drag and Drop (MUST use ActionChains)
```python
source = driver.find_element(By.ID, "draggable")
target = driver.find_element(By.ID, "droppable")

ActionChains(driver).drag_and_drop(source, target).perform()
```

## 🔧 Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure test settings in `testsetting.json`:
```json
{
  "base_url": "https://your-test-site.com",
  "credentials": {
    "username": "your_username",
    "password": "your_password"
  }
}
```

3. Run tests:
```bash
# Run all tests
pytest

# Run specific test file
pytest practice/test_movehover.py

# Run with verbose output
pytest -v
```

## 📝 Key Concepts

### ActionChains Methods
- `move_to_element(element)` - Hover over element
- `click(element)` - Click element
- `context_click(element)` - Right click
- `double_click(element)` - Double click
- `drag_and_drop(source, target)` - Drag and drop
- `key_down(key)` / `key_up(key)` - Press and hold keys
- `perform()` - **Required** to execute actions

### Important Notes
1. **Always call `.perform()`** when using ActionChains
2. Use ActionChains **only when necessary** (hover, drag, right-click, etc.)
3. For simple interactions, use regular methods (faster and simpler)

## 📚 Resources

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [ActionChains API Reference](https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains)

## 🤝 Contributing

Feel free to add more examples and documentation to help explain Selenium concepts!

---

**Tóm tắt**: `ActionChains` dùng cho hover, drag-drop, right-click - những thao tác mà `click()` thông thường không làm được!
