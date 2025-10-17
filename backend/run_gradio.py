import subprocess
import sys
import time
import threading

def run_gradio():
    try:
        # Chạy gradio_app.py
        process = subprocess.Popen(
            [sys.executable, "gradio_app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        # Đọc output theo dòng
        for line in iter(process.stdout.readline, ''):
            print(line.rstrip())
            # Tìm URL công khai
            if "Running on public URL:" in line:
                public_url = line.split("Running on public URL:")[1].strip()
                print(f"\n🎉 URL CÔNG KHAI: {public_url}")
                break
            elif "ngrok.io" in line:
                print(f"\n🎉 URL CÔNG KHAI: {line.strip()}")
                break

    except KeyboardInterrupt:
        print("\nĐang dừng ứng dụng...")
        process.terminate()
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    run_gradio()
