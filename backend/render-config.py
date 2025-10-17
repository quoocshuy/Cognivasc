"""
Render-specific configuration for Cognivasc Backend
"""

import os
from pathlib import Path

# =============================================================================
# RENDER ENVIRONMENT DETECTION
# =============================================================================
IS_RENDER = os.getenv("RENDER") is not None
IS_PRODUCTION = os.getenv("ENVIRONMENT") == "production"

# =============================================================================
# RENDER-SPECIFIC SETTINGS
# =============================================================================
if IS_RENDER:
    # Render automatically sets PORT
    PORT = int(os.getenv("PORT", 8000))
    HOST = "0.0.0.0"

    # Render free tier optimizations
    WORKERS = 1  # Single worker for free tier
    LOG_LEVEL = "INFO"

    # CORS for Render
    CORS_ORIGINS = [
        "https://cognivasc-frontend.onrender.com",
        "https://cognivasc.vercel.app",
        "http://localhost:3000",  # For local development
        "http://localhost:5173"   # For Vite dev server
    ]

    # Performance settings for Render free tier
    PREDICTION_TIMEOUT = 60  # 60 seconds
    MODEL_LOAD_TIMEOUT = 120  # 2 minutes
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    # Model path
    MODEL_PATH = Path(__file__).parent / "anemia_model.keras"

    print(f"🚀 Running on Render")
    print(f"   Host: {HOST}")
    print(f"   Port: {PORT}")
    print(f"   Model: {MODEL_PATH}")
    print(f"   CORS Origins: {CORS_ORIGINS}")

else:
    # Local development settings
    PORT = int(os.getenv("API_PORT", 8000))
    HOST = os.getenv("API_HOST", "0.0.0.0")
    WORKERS = int(os.getenv("API_WORKERS", 1))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    PREDICTION_TIMEOUT = int(os.getenv("PREDICTION_TIMEOUT", 30))
    MODEL_LOAD_TIMEOUT = int(os.getenv("MODEL_LOAD_TIMEOUT", 60))
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))

    MODEL_PATH = Path(__file__).parent / "anemia_model.keras"

    print(f"🏠 Running locally")
    print(f"   Host: {HOST}")
    print(f"   Port: {PORT}")

# =============================================================================
# EXPORT CONFIGURATION
# =============================================================================
RENDER_CONFIG = {
    "is_render": IS_RENDER,
    "is_production": IS_PRODUCTION,
    "host": HOST,
    "port": PORT,
    "workers": WORKERS,
    "log_level": LOG_LEVEL,
    "cors_origins": CORS_ORIGINS,
    "prediction_timeout": PREDICTION_TIMEOUT,
    "model_load_timeout": MODEL_LOAD_TIMEOUT,
    "max_file_size": MAX_FILE_SIZE,
    "model_path": str(MODEL_PATH)
}
