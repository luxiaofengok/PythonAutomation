"""
Scheduler để tự động chạy web_perkin.py theo lịch
Chạy file này để kích hoạt scheduler
"""
import schedule
import time
from datetime import datetime
import subprocess
import os

# ==================== CÀI ĐẶT LỊCH ====================
RUN_TIME = "08:00"  # Thời gian chạy (24h format: "08:00" = 8h sáng)
# ======================================================

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "web_perkin.py")

def run_automation():
    """Chạy automation script"""
    print(f"\n{'='*60}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting automation...")
    print(f"{'='*60}\n")
    
    try:
        # Chạy script
        result = subprocess.run(
            ["python", SCRIPT_PATH],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        
        print(result.stdout)
        if result.stderr:
            print(f"Errors:\n{result.stderr}")
        
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Automation completed!")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"[ERROR] Failed to run automation: {str(e)}")

def main():
    print("="*60)
    print("PERKIN AUTOMATION SCHEDULER")
    print("="*60)
    print(f"Script: {SCRIPT_PATH}")
    print(f"Scheduled time: {RUN_TIME} (8h sáng mỗi ngày)")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print("\nScheduler is running... Press Ctrl+C to stop")
    print("="*60)
    
    # Đăng ký lịch
    schedule.every().day.at(RUN_TIME).do(run_automation)
    
    # Hiển thị lịch chạy tiếp theo
    next_run = schedule.next_run()
    if next_run:
        print(f"\nNext run: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Vòng lặp chờ
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check mỗi phút
    except KeyboardInterrupt:
        print("\n\n[STOPPED] Scheduler đã dừng!")

if __name__ == "__main__":
    main()
