#!/usr/bin/env python3
"""
Script test API Cognivasc Anemia Detection
"""

import requests
import json
import time
import sys
from pathlib import Path

def test_health(base_url="http://localhost:8000"):
    """Test health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Model ready: {data['model']['ready']}")
            print(f"   Load time: {data['model']['load_time']:.2f}s")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check error: {e}")
        return False

def test_root(base_url="http://localhost:8000"):
    """Test root endpoint."""
    print("🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint passed")
            print(f"   Message: {data['message']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_prediction(base_url="http://localhost:8000", image_path=None):
    """Test prediction endpoint."""
    print("🔍 Testing prediction endpoint...")

    # Tìm ảnh test
    if image_path is None:
        test_images = [
            "dataset/test/anemia/1.jpg",
            "dataset/test/non-anemia/1.jpg",
            "dataset_old/test/anemia/1.jpg",
            "dataset_old/test/non-anemia/1.jpg"
        ]

        for img_path in test_images:
            if Path(img_path).exists():
                image_path = img_path
                break

    if image_path is None or not Path(image_path).exists():
        print("❌ No test image found")
        print("   Please provide a test image or place one in dataset/test/")
        return False

    try:
        with open(image_path, "rb") as f:
            files = {"file": f}
            start_time = time.time()
            response = requests.post(f"{base_url}/predict", files=files, timeout=30)
            end_time = time.time()

            if response.status_code == 200:
                data = response.json()
                print("✅ Prediction test passed")
                print(f"   Image: {image_path}")
                print(f"   Result: {data['label']}")
                print(f"   Confidence: {data['confidence']}")
                print(f"   Response time: {end_time - start_time:.2f}s")
                return True
            else:
                print(f"❌ Prediction test failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Prediction test error: {e}")
        return False

def test_invalid_file(base_url="http://localhost:8000"):
    """Test với file không hợp lệ."""
    print("🔍 Testing invalid file handling...")
    try:
        # Tạo file text giả
        files = {"file": ("test.txt", "This is not an image", "text/plain")}
        response = requests.post(f"{base_url}/predict", files=files, timeout=10)

        if response.status_code == 400:
            print("✅ Invalid file handling passed")
            return True
        else:
            print(f"❌ Invalid file handling failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Invalid file test error: {e}")
        return False

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Test Cognivasc API")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--image", help="Path to test image")
    parser.add_argument("--skip-prediction", action="store_true", help="Skip prediction test")

    args = parser.parse_args()

    print("=" * 60)
    print("🧪 COGNIVASC API TEST SUITE")
    print("=" * 60)
    print(f"Testing API at: {args.url}")
    print("=" * 60)

    tests_passed = 0
    total_tests = 0

    # Test 1: Health check
    total_tests += 1
    if test_health(args.url):
        tests_passed += 1
    print()

    # Test 2: Root endpoint
    total_tests += 1
    if test_root(args.url):
        tests_passed += 1
    print()

    # Test 3: Invalid file
    total_tests += 1
    if test_invalid_file(args.url):
        tests_passed += 1
    print()

    # Test 4: Prediction (optional)
    if not args.skip_prediction:
        total_tests += 1
        if test_prediction(args.url, args.image):
            tests_passed += 1
        print()

    # Kết quả
    print("=" * 60)
    print(f"📊 TEST RESULTS: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("🎉 All tests passed! API is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the API.")
        sys.exit(1)

if __name__ == "__main__":
    main()
