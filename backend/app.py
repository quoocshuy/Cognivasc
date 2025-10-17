from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import io, os
import logging
import sys
from typing import Optional
import time

# =============================================================================
# CẤU HÌNH MODEL
# =============================================================================
from config import (
    BASE_DIR, MODEL_PATH, IMG_SIZE, OPTIMIZED_THRESHOLD, CLASS_NAMES,
    HOST, PORT, WORKERS, LOG_LEVEL, LOG_FORMAT,
    CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS,
    MAX_FILE_SIZE, ALLOWED_EXTENSIONS, MIN_IMAGE_SIZE,
    PREDICTION_TIMEOUT, MODEL_LOAD_TIMEOUT
)

# Cấu hình logging để tránh lỗi encoding
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global model variable
model: Optional[tf.keras.Model] = None
model_loaded: bool = False
model_load_time: Optional[float] = None

# =============================================================================
# MODEL LOADING FUNCTIONS
# =============================================================================
def load_model() -> bool:
    """Tải model và trả về True nếu thành công, False nếu thất bại."""
    global model, model_loaded, model_load_time

    logger.info("=" * 50)
    logger.info("INITIALIZING ANEMIA DETECTION MODEL")
    logger.info("=" * 50)

    start_time = time.time()

    # Kiểm tra file model tồn tại
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Model file not found: {MODEL_PATH}")
        logger.error(f"   Current working directory: {os.getcwd()}")
        logger.error(f"   Base directory: {BASE_DIR}")
        return False

    logger.info(f"Model file found: {MODEL_PATH}")
    logger.info(f"File size: {os.path.getsize(MODEL_PATH) / (1024*1024):.2f} MB")

    try:
        # Tải model
        logger.info("Loading model...")
        model = tf.keras.models.load_model(MODEL_PATH)

        # Kiểm tra model đã tải thành công
        if model is None:
            logger.error("Model loaded but is None")
            return False

        # Test model với input mẫu
        logger.info("Testing model with sample input...")
        test_input = np.random.random((1, 224, 224, 3)).astype(np.float32)
        test_output = model.predict(test_input, verbose=0)

        if test_output is None or len(test_output) == 0:
            logger.error("Model test failed - no output")
            return False

        model_load_time = time.time() - start_time
        model_loaded = True

        logger.info("Model loaded successfully!")
        logger.info(f"Load time: {model_load_time:.2f} seconds")
        logger.info(f"Model input shape: {model.input_shape}")
        logger.info(f"Model output shape: {model.output_shape}")
        logger.info(f"Model parameters: {model.count_params():,}")
        logger.info("=" * 50)

        return True

    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        logger.error(f"   Error type: {type(e).__name__}")
        model = None
        model_loaded = False
        return False

def validate_model_ready() -> bool:
    """Kiểm tra model có sẵn sàng để sử dụng không."""
    return model_loaded and model is not None

# =============================================================================
# XỬ LÝ ẢNH
# =============================================================================
def preprocess_image(img_pil):
    """Tiền xử lý ảnh PIL đầu vào để phù hợp với model."""
    img_pil = img_pil.convert("RGB")  # ✅ thêm để thống nhất
    img_np = np.array(img_pil).astype('uint8')

    if len(img_np.shape) == 2 or img_np.shape[2] == 1:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
    if img_np.shape[2] == 4:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)

    img_resized = cv2.resize(img_np, IMG_SIZE)
    img_expanded = np.expand_dims(img_resized, axis=0)
    return tf.keras.applications.mobilenet_v3.preprocess_input(img_expanded)

# =============================================================================
# DỰ ĐOÁN
# =============================================================================
def run_prediction(img_pil):
    if model is None:
        raise ValueError("Model chưa được tải thành công.")

    processed_input = preprocess_image(img_pil)
    raw_prob = model.predict(processed_input)[0][0]  # P(non-anemia)
    anemia_score = 1 - raw_prob                      # P(anemia)

    # ✅ Debug log giống hệt gradio.py
    logger.info("-" * 30)
    logger.info(f"[DEBUG] raw_prob (P[non-anemia]): {raw_prob:.4f}")
    logger.info(f"[DEBUG] anemia_score (P[anemia]): {anemia_score:.4f}")
    logger.info(f"[DEBUG] Threshold: {OPTIMIZED_THRESHOLD}")

    if anemia_score > OPTIMIZED_THRESHOLD:
        label = "Nghi ngờ Thiếu máu"
        advice_text = (
            "<b>Kết quả: Có dấu hiệu Thiếu máu</b><br>"
            "Khuyên bạn nên tham khảo ý kiến bác sĩ sớm."
        )
    else:
        label = "Không nghi ngờ Thiếu máu"
        advice_text = (
            "<b>Kết quả: Không có dấu hiệu Thiếu máu</b><br>"
            "Hãy duy trì lối sống lành mạnh và khám sức khỏe định kỳ."
        )

    logger.info(f"[DEBUG] Conclusion: {label}")
    logger.info("-" * 30)

    return {
        "label": label,
        "advice": advice_text,
        "confidence": {
            "Thiếu máu": float(anemia_score),
            "Không Thiếu máu": float(raw_prob)
        }
    }

# =============================================================================
# STARTUP/SHUTDOWN EVENTS
# =============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Quản lý lifecycle của FastAPI app."""
    # Startup
    logger.info("Starting Cognivasc Anemia Detection API...")

    # Tải model khi khởi động
    if not load_model():
        logger.error("CRITICAL: Model failed to load. Server will start but predictions will fail.")
        logger.error("   Please check model file and restart the server.")
    else:
        logger.info("Server ready to accept requests!")

    yield

    # Shutdown
    logger.info("Shutting down server...")
    global model
    model = None

# =============================================================================
# FASTAPI APP
# =============================================================================
app = FastAPI(
    title="Cognivasc Anemia Detection API",
    description="REST API cho hệ thống dự đoán thiếu máu qua ảnh kết mạc",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# =============================================================================
# ENDPOINTS
# =============================================================================
@app.get("/")
async def root():
    """Root endpoint với thông tin API."""
    return {
        "message": "Cognivasc Anemia Detection API",
        "version": "1.0.0",
        "status": "running",
        "model_ready": validate_model_ready(),
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint để kiểm tra trạng thái server và model."""
    health_status = {
        "status": "healthy" if validate_model_ready() else "unhealthy",
        "timestamp": time.time(),
        "model": {
            "loaded": model_loaded,
            "ready": validate_model_ready(),
            "load_time": model_load_time,
            "path": MODEL_PATH,
            "exists": os.path.exists(MODEL_PATH)
        },
        "server": {
            "uptime": time.time() - (model_load_time or 0),
            "version": "1.0.0"
        }
    }

    status_code = 200 if validate_model_ready() else 503
    return JSONResponse(content=health_status, status_code=status_code)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Endpoint dự đoán thiếu máu từ ảnh kết mạc."""

    # Kiểm tra model có sẵn sàng không
    if not validate_model_ready():
        raise HTTPException(
            status_code=503,
            detail="Model is not ready. Please check server health at /health"
        )

    # Kiểm tra file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )

    try:
        logger.info(f"Processing image: {file.filename} ({file.content_type})")

        contents = await file.read()
        img = Image.open(io.BytesIO(contents))

        # Kiểm tra kích thước ảnh
        if img.size[0] < MIN_IMAGE_SIZE[0] or img.size[1] < MIN_IMAGE_SIZE[1]:
            raise HTTPException(
                status_code=400,
                detail=f"Image too small. Minimum size: {MIN_IMAGE_SIZE[0]}x{MIN_IMAGE_SIZE[1]} pixels"
            )

        result = run_prediction(img)
        logger.info(f"Prediction completed for {file.filename}")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in prediction process: {str(e)}")
        logger.error(f"   Error type: {type(e).__name__}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("COGNIVASC ANEMIA DETECTION API")
    print("=" * 60)
    print("Server Information:")
    print(f"   - Host: {HOST}")
    print(f"   - Port: {PORT}")
    print(f"   - Model: {MODEL_PATH}")
    print(f"   - Threshold: {OPTIMIZED_THRESHOLD}")
    print("=" * 60)
    print("Available Endpoints:")
    print(f"   - Root: http://{HOST}:{PORT}/")
    print(f"   - Health: http://{HOST}:{PORT}/health")
    print(f"   - Predict: http://{HOST}:{PORT}/predict")
    print(f"   - Docs: http://{HOST}:{PORT}/docs")
    print(f"   - Redoc: http://{HOST}:{PORT}/redoc")
    print("=" * 60)
    print("Starting server...")
    print("=" * 60)

    try:
        uvicorn.run(
            app,
            host=HOST,
            port=PORT,
            log_level=LOG_LEVEL.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"\nServer failed to start: {e}")
        sys.exit(1)

# =============================================================================
# HƯỚNG DẪN SỬ DỤNG
# =============================================================================
"""
🚀 CÁCH CHẠY SERVER:

1. Chạy trực tiếp:
   python app.py

2. Chạy với uvicorn:
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload

3. Chạy với gunicorn (production):
   gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

🔍 KIỂM TRA TRẠNG THÁI:

1. Health check:
   curl http://localhost:8000/health

2. API documentation:
   http://localhost:8000/docs

3. Test prediction:
   curl -X POST "http://localhost:8000/predict" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@test_image.jpg"

📝 LƯU Ý:
- Model sẽ được tải tự động khi khởi động server
- Nếu model không tải được, server vẫn chạy nhưng /predict sẽ trả về lỗi 503
- Sử dụng /health để kiểm tra trạng thái model
- API hỗ trợ CORS cho frontend
"""
