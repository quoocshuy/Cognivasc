"""
Cấu hình cho Cognivasc Anemia Detection API
"""

import os
from pathlib import Path

# =============================================================================
# ĐƯỜNG DẪN VÀ FILE
# =============================================================================
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "anemia_model.keras"
DATASET_DIR = BASE_DIR / "dataset"

# =============================================================================
# CẤU HÌNH MODEL
# =============================================================================
IMG_SIZE = (224, 224)
OPTIMIZED_THRESHOLD = 0.1641
CLASS_NAMES = ['anemia', 'non-anemia']

# =============================================================================
# CẤU HÌNH SERVER
# =============================================================================
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_WORKERS = 1

# Cấu hình từ environment variables
HOST = os.getenv("API_HOST", DEFAULT_HOST)
PORT = int(os.getenv("API_PORT", DEFAULT_PORT))
WORKERS = int(os.getenv("API_WORKERS", DEFAULT_WORKERS))

# Render-specific configuration
if os.getenv("RENDER"):
    # Render automatically sets PORT environment variable
    PORT = int(os.getenv("PORT", DEFAULT_PORT))
    HOST = "0.0.0.0"  # Render requires 0.0.0.0

# =============================================================================
# CẤU HÌNH LOGGING
# =============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# =============================================================================
# CẤU HÌNH CORS
# =============================================================================
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Render-specific CORS configuration
if os.getenv("RENDER"):
    # Allow Render frontend URLs
    render_frontend = os.getenv("RENDER_FRONTEND_URL", "")
    if render_frontend:
        CORS_ORIGINS = [render_frontend, "https://cognivasc-frontend.onrender.com"]
    else:
        CORS_ORIGINS = ["*"]

# =============================================================================
# CẤU HÌNH UPLOAD
# =============================================================================
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
MIN_IMAGE_SIZE = (50, 50)

# =============================================================================
# CẤU HÌNH PERFORMANCE
# =============================================================================
PREDICTION_TIMEOUT = int(os.getenv("PREDICTION_TIMEOUT", 30))  # seconds
MODEL_LOAD_TIMEOUT = int(os.getenv("MODEL_LOAD_TIMEOUT", 60))  # seconds

# Render-specific performance configuration
if os.getenv("RENDER"):
    # Render free tier has limited resources
    PREDICTION_TIMEOUT = int(os.getenv("PREDICTION_TIMEOUT", 60))  # Increase timeout
    MODEL_LOAD_TIMEOUT = int(os.getenv("MODEL_LOAD_TIMEOUT", 120))  # Increase load timeout

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================
def validate_config():
    """Kiểm tra cấu hình có hợp lệ không."""
    errors = []

    # Kiểm tra model file
    if not MODEL_PATH.exists():
        errors.append(f"Model file not found: {MODEL_PATH}")

    # Kiểm tra port
    if not (1 <= PORT <= 65535):
        errors.append(f"Invalid port: {PORT}")

    # Kiểm tra workers
    if WORKERS < 1:
        errors.append(f"Invalid workers count: {WORKERS}")

    # Kiểm tra threshold
    if not (0 <= OPTIMIZED_THRESHOLD <= 1):
        errors.append(f"Invalid threshold: {OPTIMIZED_THRESHOLD}")

    return errors

def get_config_summary():
    """Lấy tóm tắt cấu hình."""
    return {
        "model": {
            "path": str(MODEL_PATH),
            "exists": MODEL_PATH.exists(),
            "threshold": OPTIMIZED_THRESHOLD,
            "image_size": IMG_SIZE,
            "classes": CLASS_NAMES
        },
        "server": {
            "host": HOST,
            "port": PORT,
            "workers": WORKERS
        },
        "upload": {
            "max_file_size": MAX_FILE_SIZE,
            "allowed_extensions": list(ALLOWED_EXTENSIONS),
            "min_image_size": MIN_IMAGE_SIZE
        },
        "performance": {
            "prediction_timeout": PREDICTION_TIMEOUT,
            "model_load_timeout": MODEL_LOAD_TIMEOUT
        }
    }

if __name__ == "__main__":
    # Test cấu hình
    print("Validating configuration...")
    errors = validate_config()

    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("Configuration is valid")

    print("\nConfiguration Summary:")
    import json
    print(json.dumps(get_config_summary(), indent=2))
