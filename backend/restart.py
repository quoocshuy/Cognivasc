#!/usr/bin/env python3
"""
Script restart server Cognivasc Anemia Detection API
Tự động kill process cũ và chạy lại server
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("RESTARTING COGNIVASC ANEMIA DETECTION API")
    print("=" * 60)

    # Thay đổi thư mục làm việc
    script_dir = Path(__file__).parent
    import os
    os.chdir(script_dir)

    try:
        # Chạy start_server.py với --force để kill port cũ
        result = subprocess.run([
            sys.executable, "start_server.py", "--force"
        ], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Failed to restart server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nRestart cancelled by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
