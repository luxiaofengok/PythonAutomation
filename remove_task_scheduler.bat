@echo off
echo ============================================================
echo XÓA TASK SCHEDULER - PERKIN AUTOMATION
echo ============================================================
echo.

echo Đang xóa task "PerkinAutomation"...
schtasks /delete /tn "PerkinAutomation" /f

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Đã xóa task thành công!
) else (
    echo.
    echo [INFO] Task không tồn tại hoặc đã bị xóa.
)

echo.
pause
