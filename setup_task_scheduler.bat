@echo off
echo ============================================================
echo WINDOWS TASK SCHEDULER SETUP - PERKIN AUTOMATION
echo ============================================================
echo.

REM Lấy đường dẫn đầy đủ
set SCRIPT_PATH=%~dp0web_perkin.py
set PYTHON_PATH=python

echo [INFO] Script path: %SCRIPT_PATH%
echo [INFO] Python path: %PYTHON_PATH%
echo.

REM Xóa task cũ nếu có
echo [1] Xóa task cũ (nếu có)...
schtasks /delete /tn "PerkinAutomation" /f >nul 2>&1

REM Tạo task mới
echo [2] Tạo task mới...
schtasks /create /tn "PerkinAutomation" /tr "\"%PYTHON_PATH%\" \"%SCRIPT_PATH%\"" /sc daily /st 08:00 /rl highest /f

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo SETUP THÀNH CÔNG!
    echo ============================================================
    echo.
    echo Task Name: PerkinAutomation
    echo Schedule: Mỗi ngày lúc 8:00 sáng
    echo Script: %SCRIPT_PATH%
    echo.
    echo Để xem task:
    echo   schtasks /query /tn "PerkinAutomation" /fo list /v
    echo.
    echo Để chạy ngay:
    echo   schtasks /run /tn "PerkinAutomation"
    echo.
    echo Để xóa task:
    echo   schtasks /delete /tn "PerkinAutomation" /f
    echo.
) else (
    echo.
    echo [ERROR] Có lỗi xảy ra! Chạy file này với quyền Administrator.
    echo.
)

pause
