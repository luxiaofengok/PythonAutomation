@echo off
echo ============================================================
echo PERKIN AUTOMATION - AUTO STARTUP SETUP
echo ============================================================
echo.

REM Cài đặt thư viện schedule nếu chưa có
echo [1] Đang cài đặt thư viện schedule...
pip install schedule

echo.
echo [2] Tạo shortcut vào Startup folder...

REM Tạo VBS script để chạy Python không hiện console
echo Set WshShell = CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo Set oShellLink = WshShell.CreateShortcut("%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Perkin_Scheduler.lnk") >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.TargetPath = "pythonw.exe" >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.Arguments = """%~dp0scheduler_perkin.py""" >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.WorkingDirectory = "%~dp0" >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.WindowStyle = 7 >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.Description = "Perkin Automation Scheduler - Runs at 8 AM daily" >> "%TEMP%\CreateShortcut.vbs"
echo oShellLink.Save >> "%TEMP%\CreateShortcut.vbs"

cscript //nologo "%TEMP%\CreateShortcut.vbs"
del "%TEMP%\CreateShortcut.vbs"

echo.
echo ============================================================
echo SETUP HOÀN TẤT!
echo ============================================================
echo.
echo Scheduler sẽ tự động chạy khi Windows khởi động
echo Code sẽ chạy lúc 8h sáng mỗi ngày
echo.
echo Để kiểm tra ngay:
echo   python scheduler_perkin.py
echo.
echo Để hủy tự động chạy:
echo   Xóa file: %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Perkin_Scheduler.lnk
echo.
pause
