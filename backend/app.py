from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import io, os

# =============================================================================
# CẤU HÌNH MODEL
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = "backend/anemia_model.keras"
IMG_SIZE = (224, 224)
OPTIMIZED_THRESHOLD = 0.1641
CLASS_NAMES = ['anemia', 'non-anemia']

import os
print(os.path.abspath(MODEL_PATH))
print(os.path.exists(MODEL_PATH))


print("Đang tải model...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model đã được tải thành công.")
except Exception as e:
    print(f"❌ Không thể tải model '{MODEL_PATH}': {e}")
    model = None

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
    print("-" * 30)
    print(f"[DEBUG] raw_prob (P[non-anemia]): {raw_prob:.4f}")
    print(f"[DEBUG] anemia_score (P[anemia]): {anemia_score:.4f}")
    print(f"[DEBUG] Ngưỡng đang sử dụng: {OPTIMIZED_THRESHOLD}")

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

    print(f"[DEBUG] Kết luận: {label}")
    print("-" * 30)

    return {
        "label": label,
        "advice": advice_text,
        "confidence": {
            "Thiếu máu": float(anemia_score),
            "Không Thiếu máu": float(raw_prob)
        }
    }

# =============================================================================
# FASTAPI APP
# =============================================================================
app = FastAPI(
    title="Cognivasc Anemia Detection API",
    description="REST API cho hệ thống dự đoán thiếu máu qua ảnh kết mạc",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# ENDPOINT
# =============================================================================
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        result = run_prediction(img)
        return result

    except Exception as e:
        print("❌ Lỗi trong quá trình dự đoán:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Chạy server: uvicorn app:app --host 0.0.0.0 --port 8000
# Test API: http://localhost:8000/docs
# API ở đây là FastAPI, đóng vai trò nhận dữ liệu (ảnh) từ frontend về và gửi vào backend
