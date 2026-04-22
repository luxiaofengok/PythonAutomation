"""
Scheduler để tự động chạy tất cả các web scripts theo lịch
Chạy web_asksurf.py đầu tiên, sau đó đợi 5 phút rồi chạy lần lượt các file web khác
"""
import schedule
import time
from datetime import datetime
import subprocess
import os

# ==================== CÀI ĐẶT LỊCH ====================
START_TIME = "19:31"  # Thời gian bắt đầu chạy (09:55 mỗi ngày)
DELAY_BETWEEN_SCRIPTS = 300  # Delay giữa các script (giây) - 5 phút
# ======================================================
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")

# Danh sách các file cần chạy theo thứ tự
WEB_SCRIPTS = [
    # "web_blend_money.py",
    # "web_neftit.py",
    # "web_onvoyage.py",
    # "web_play_providence.py",
    # "web_tria.py",
    "web_trex.py",
    "web_stormrae.py",
    "web_fairshare.py",
    "web_prismax.py",
    "web_upshot.py",
    # "web_pip_world.py",
]

def run_single_script(script_name):
    """Chạy một automation script"""
    script_path = os.path.join(WEB_DIR, script_name)
    
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running: {script_name}")
    print(f"{'='*60}\n")
    
    try:
        # Set UTF-8 encoding để tránh lỗi Unicode
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            cwd=WEB_DIR,
            env=env,
            encoding='utf-8',
            errors='replace',  # Thay thế ký tự không hiển thị được
            timeout=900  # Timeout 15 phút
        )
        
        # In output, thay thế ký tự đặc biệt nếu cần
        if result.stdout:
            try:
                print(result.stdout)
            except UnicodeEncodeError:
                print(result.stdout.encode('ascii', 'ignore').decode('ascii'))
        
        if result.stderr:
            try:
                print(f"Errors:\n{result.stderr}")
            except UnicodeEncodeError:
                print(f"Errors:\n{result.stderr.encode('ascii', 'ignore').decode('ascii')}")
        
        # Kiểm tra exit code
        success = result.returncode == 0
        status = "COMPLETED" if success else f"FAILED (exit code: {result.returncode})"
        
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {status}: {script_name}")
        print(f"{'='*60}\n")
        
        return success
        
    except subprocess.TimeoutExpired:
        print(f"\n[ERROR] {script_name} timeout sau 30 phút!\n")
        return False
    except Exception as e:
        print(f"\n[ERROR] Failed to run {script_name}: {str(e)}\n")
        return False

def run_all_scripts():
    """Chạy tất cả automation scripts theo thứ tự"""
    print(f"\n{'#'*60}")
    print(f"STARTING BATCH AUTOMATION")
    print(f"Total scripts: {len(WEB_SCRIPTS)}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*60}\n")
    
    success_count = 0
    failed_count = 0
    failed_scripts = []
    
    for i, script in enumerate(WEB_SCRIPTS, 1):
        print(f"\n>>> Script {i}/{len(WEB_SCRIPTS)}: {script}")
        
        # Chạy script
        success = run_single_script(script)
        
        # Track kết quả
        if success:
            success_count += 1
        else:
            failed_count += 1
            failed_scripts.append(script)
        
        # Nếu không phải script cuối cùng, đợi 5 phút (hoặc 2 phút nếu bị lỗi)
        if i < len(WEB_SCRIPTS):
            delay = DELAY_BETWEEN_SCRIPTS if success else 120  # Chỉ đợi 2 phút nếu bị lỗi
            print(f"\nWaiting {delay} seconds before next script...")
            time.sleep(delay)
    
    print(f"\n{'#'*60}")
    print(f"ALL SCRIPTS COMPLETED")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nSUMMARY:")
    print(f"  Success: {success_count}/{len(WEB_SCRIPTS)}")
    print(f"  Failed: {failed_count}/{len(WEB_SCRIPTS)}")
    if failed_scripts:
        print(f"\nFailed scripts:")
        for script in failed_scripts:
            print(f"  - {script}")
    print(f"{'#'*60}\n")

def main():
    print("="*60)
    print("ALL WEB AUTOMATION SCHEDULER")
    print("="*60)
    print(f"Web directory: {WEB_DIR}")
    print(f"Scheduled time: {START_TIME} (2h chiều mỗi ngày)")
    print(f"Delay between scripts: {DELAY_BETWEEN_SCRIPTS} seconds (5 phút)")
    print(f"Total scripts: {len(WEB_SCRIPTS)}")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print("\nScripts to run:")
    for i, script in enumerate(WEB_SCRIPTS, 1):
        print(f"  {i}. {script}")
    print("="*60)
    print("\nScheduler is running... Press Ctrl+C to stop")
    print("="*60)
    
    # Đăng ký lịch
    schedule.every().day.at(START_TIME).do(run_all_scripts)
    
    # Hiển thị lịch chạy tiếp theo
    next_run = schedule.next_run()
    if next_run:
        print(f"\nNext run: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Vòng lặp chờ
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # Check mỗi 30 giây
    except KeyboardInterrupt:
        print("\n\n[STOPPED] Scheduler đã dừng!")

if __name__ == "__main__":
    main()
