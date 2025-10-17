#!/usr/bin/env python3
"""
Test script để kiểm tra chức năng kill port
"""

import subprocess
import sys
import time
from pathlib import Path

def test_kill_port():
    """Test chức năng kill port."""
    print("Testing kill port functionality...")

    # Import function từ start_server.py
    sys.path.append(str(Path(__file__).parent))
    from start_server import kill_process_on_port

    # Test kill port 8000
    print("\n1. Testing kill port 8000...")
    kill_process_on_port(8000)

    # Test kill port 9000 (không có process)
    print("\n2. Testing kill port 9000 (should be empty)...")
    kill_process_on_port(9000)

    print("\nTest completed!")

if __name__ == "__main__":
    test_kill_port()
