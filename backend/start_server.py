#!/usr/bin/env python3
"""
Script khởi động server Cognivasc Anemia Detection API
"""

import os
import sys
import subprocess
import argparse
import platform
import time
from pathlib import Path

def check_requirements():
    """Kiểm tra các yêu cầu cần thiết."""
    print("Checking requirements...")

    # Kiểm tra Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8+ is required")
        return False

    # Kiểm tra file model
    model_path = Path("anemia_model.keras")
    if not model_path.exists():
        print(f"ERROR: Model file not found: {model_path.absolute()}")
        return False

    # Kiểm tra requirements.txt
    req_path = Path("requirements.txt")
    if not req_path.exists():
        print(f"ERROR: Requirements file not found: {req_path.absolute()}")
        return False

    print("All requirements satisfied")
    return True

def kill_process_on_port(port):
    """Kill process đang chạy trên port cụ thể."""
    print(f"Checking for processes on port {port}...")

    try:
        # Tìm process trên port
        if platform.system() == "Windows":
            # Windows
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True,
                check=True
            )

            pids = []
            for line in result.stdout.split('\n'):
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        if pid.isdigit():
                            pids.append(pid)

            # Kill các process
            killed_count = 0
            for pid in pids:
                try:
                    subprocess.run(
                        ["taskkill", "/PID", pid, "/F"],
                        capture_output=True,
                        check=True
                    )
                    print(f"Killed process {pid} on port {port}")
                    killed_count += 1
                except subprocess.CalledProcessError:
                    print(f"Failed to kill process {pid}")

            if killed_count > 0:
                print(f"Killed {killed_count} process(es) on port {port}")
                time.sleep(2)  # Đợi port được giải phóng
            else:
                print(f"No processes found on port {port}")

        else:
            # Linux/Mac
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                text=True
            )

            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        subprocess.run(["kill", "-9", pid], check=True)
                        print(f"Killed process {pid} on port {port}")
                    except subprocess.CalledProcessError:
                        print(f"Failed to kill process {pid}")

                print(f"Killed {len(pids)} process(es) on port {port}")
                time.sleep(2)
            else:
                print(f"No processes found on port {port}")

    except subprocess.CalledProcessError as e:
        print(f"Error checking port {port}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def install_dependencies():
    """Cài đặt dependencies nếu cần."""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                      check=True, capture_output=True, text=True)
        print("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        print(f"   Error: {e.stderr}")
        return False

def start_server(host="0.0.0.0", port=8000, reload=False, workers=1, auto_kill_port=True):
    """Khởi động server."""
    print(f"Starting server on {host}:{port}")

    cmd = [
        sys.executable, "-m", "uvicorn",
        "app:app",
        "--host", host,
        "--port", str(port)
    ]

    if reload:
        cmd.append("--reload")
        print("Auto-reload enabled")

    if workers > 1:
        cmd.extend(["--workers", str(workers)])
        print(f"Using {workers} workers")

    max_retries = 2
    for attempt in range(max_retries):
        try:
            # Chạy server và chờ nó chạy (blocking)
            subprocess.run(cmd, check=True)
            return True
        except KeyboardInterrupt:
            print("\nServer stopped by user")
            return True
        except subprocess.CalledProcessError as e:
            error_msg = str(e).lower()
            if "address already in use" in error_msg or "bind" in error_msg:
                if auto_kill_port and attempt < max_retries - 1:
                    print(f"Port {port} is already in use. Attempting to kill existing processes...")
                    kill_process_on_port(port)
                    print("Retrying to start server...")
                    continue
                else:
                    print(f"Port {port} is already in use. Use --kill-port to automatically kill existing processes.")
                    return False
            else:
                print(f"Server failed to start: {e}")
                return False

    return False

def main():
    parser = argparse.ArgumentParser(description="Start Cognivasc Anemia Detection API")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to (default: 8000)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes (default: 1)")
    parser.add_argument("--install", action="store_true", help="Install dependencies before starting")
    parser.add_argument("--skip-check", action="store_true", help="Skip requirement checks")
    parser.add_argument("--kill-port", action="store_true", help="Kill existing processes on the port before starting")
    parser.add_argument("--force", action="store_true", help="Force kill port and restart (equivalent to --kill-port)")

    args = parser.parse_args()

    print("=" * 60)
    print("COGNIVASC ANEMIA DETECTION API")
    print("=" * 60)

    # Thay đổi thư mục làm việc
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Kill process trên port nếu được yêu cầu
    if args.kill_port or args.force:
        kill_process_on_port(args.port)

    # Kiểm tra requirements
    if not args.skip_check and not check_requirements():
        print("Requirements check failed")
        sys.exit(1)

    # Cài đặt dependencies nếu cần
    if args.install:
        if not install_dependencies():
            print("Failed to install dependencies")
            sys.exit(1)

    # Khởi động server
    auto_kill = args.kill_port or args.force  # Tự động kill port nếu có lỗi
    if not start_server(args.host, args.port, args.reload, args.workers, auto_kill):
        sys.exit(1)

if __name__ == "__main__":
    main()
