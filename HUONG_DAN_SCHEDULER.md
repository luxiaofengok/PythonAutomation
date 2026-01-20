# Hướng Dẫn Lên Lịch Tự Động

## 🕐 Tự động chạy lúc 8h sáng mỗi ngày

### ⭐ Cách 1: Windows Task Scheduler (KHUYÊN DÙNG)

**Ưu điểm:** Không tốn RAM, ổn định nhất, tích hợp Windows

1. **Click chuột phải vào:** `setup_task_scheduler.bat` → **"Run as Administrator"**
2. **Xong!** Windows sẽ tự động chạy code lúc 8h sáng mỗi ngày
3. Không cần bật Python suốt

**Kiểm tra task:**
```bash
schtasks /query /tn "PerkinAutomation" /fo list /v
```

**Chạy thử ngay:**
```bash
schtasks /run /tn "PerkinAutomation"
```

**Xóa task (nếu không dùng nữa):**
- Click đúp: `remove_task_scheduler.bat`

---

### Cách 2: Tự động chạy khi khởi động Windows

**Ưu điểm:** Đơn giản, không cần quyền Admin

1. **Click đúp vào file:** `setup_scheduler.bat`
2. **Xong!** Scheduler sẽ tự động chạy mỗi khi Windows khởi động
3. Code sẽ tự chạy lúc 8h sáng mỗi ngày

**Lưu ý:** Python chạy ngầm suốt để đợi đến 8h

---

### Cách 3: Chạy thủ công scheduler

```bash
python scheduler_perkin.py
```

**Lưu ý:** Giữ cửa sổ terminal mở

---

## ⚙️ Tùy chỉnh thời gian

Mở file `scheduler_perkin.py` và sửa:

```python
RUN_TIME = "08:00"  # Đổi thành giờ bạn muốn (VD: "14:30" = 2h30 chiều)
```

### Ví dụ:
- `"09:00"` - 9h sáng
- `"14:30"` - 2h30 chiều  
- `"20:00"` - 8h tối

---

## 🛑 Dừng scheduler

### Nếu dùng Cách 1 (Task Scheduler):
- Chạy file: `remove_task_scheduler.bat`
- Hoặc dùng lệnh: `schtasks /delete /tn "PerkinAutomation" /f`

### Nếu dùng Cách 2 (Startup):
Xóa file shortcut:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Perkin_Scheduler.lnk
```

### Nếu dùng Cách 3 (Thủ công):
Nhấn `Ctrl + C` trong terminal

---

## 📊 So sánh các cách

| | Cách 1: Task Scheduler | Cách 2: Startup | Cách 3: Thủ công |
|---|---|---|---|
| **Ổn định** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Tốn RAM** | Không | Có (chút ít) | Có |
| **Cần Admin** | Có (1 lần) | Không | Không |
| **Tự động** | ✅ | ✅ | ❌ |

**Khuyến nghị:** Dùng **Cách 1** (Task Scheduler) - Tốt nhất!

---

## 📋 Kiểm tra lịch

Sau khi chạy `scheduler_perkin.py`, nó sẽ hiển thị:
- Thời gian chạy tiếp theo
- Trạng thái scheduler

---

## ⚠️ Lưu ý

- Máy tính phải bật vào lúc 8h sáng để code chạy
- Nếu máy đang sleep/hibernate thì sẽ không chạy
- Để chạy ngay lập tức (test): `python web_perkin.py`
