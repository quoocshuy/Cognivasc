# 🚀 Deploy Backend trên Vercel

## ⚠️ **Hạn Chế Vercel cho Backend:**

### **❌ Vấn đề:**
- **10s execution limit** - Model AI có thể cần nhiều thời gian hơn
- **50MB function size limit** - Model 4.8MB + dependencies có thể vượt quá
- **Serverless functions** - Không phù hợp với persistent model loading
- **Cold start** - Model phải load lại mỗi lần request

### **✅ Có thể làm được nhưng cần tối ưu:**

---

## 🛠️ **Cấu Hình Vercel Backend:**

### **1. Requirements (vercel-requirements.txt)**
```txt
fastapi
uvicorn[standard]
tensorflow-cpu
pillow
numpy
opencv-python-headless
python-multipart
```

### **2. API Handler (api/vercel_handler.py)**
- Serverless function handler
- Xử lý CORS
- Route requests đến FastAPI app

### **3. Vercel Config (vercel.json)**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/vercel_handler.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/vercel_handler.py"
    }
  ],
  "functions": {
    "api/vercel_handler.py": {
      "maxDuration": 10
    }
  }
}
```

---

## 🚀 **Hướng Dẫn Deploy:**

### **Bước 1: Chuẩn bị**
```bash
# Đảm bảo có các files:
# - backend/vercel-requirements.txt
# - backend/api/vercel_handler.py
# - backend/vercel.json
```

### **Bước 2: Deploy Backend**
1. Truy cập [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import GitHub repository
4. **Root Directory**: `backend`
5. **Framework Preset**: Other
6. **Build Command**: `pip install -r vercel-requirements.txt`
7. **Output Directory**: (để trống)

### **Bước 3: Environment Variables**
```env
PYTHON_VERSION=3.11
```

### **Bước 4: Deploy Frontend**
1. **Root Directory**: `frontend`
2. **Build Command**: `npm install && npm run build`
3. **Output Directory**: `dist`
4. **Environment Variable**: `VITE_API_URL=https://your-backend-url.vercel.app`

---

## 🔧 **Tối Ưu cho Vercel:**

### **1. Model Optimization**
```python
# Lazy loading model
model = None

def get_model():
    global model
    if model is None:
        model = tf.keras.models.load_model(MODEL_PATH)
    return model
```

### **2. Memory Management**
```python
# Clear cache after prediction
import gc
gc.collect()
```

### **3. Timeout Handling**
```python
# Set timeout cho prediction
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Prediction timeout")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(8)  # 8 seconds timeout
```

---

## 📊 **So Sánh Platforms:**

| Platform | Execution Time | Memory | Model Size | Best For |
|----------|----------------|--------|------------|----------|
| **Vercel** | 10s | 1GB | <50MB | Simple APIs |
| **Render** | Unlimited | 512MB | Unlimited | AI Models |
| **Fly.io** | Unlimited | 256MB | Unlimited | Performance |
| **Netlify** | 10s | 1GB | <50MB | Simple Functions |

---

## 🎯 **Khuyến Nghị:**

### **✅ Sử dụng Vercel nếu:**
- Model nhỏ (<10MB)
- Prediction nhanh (<5s)
- Ít requests
- Demo/Testing

### **❌ Không nên dùng Vercel nếu:**
- Model lớn (>20MB)
- Prediction chậm (>5s)
- Nhiều requests
- Production

---

## 🚀 **Alternative Solutions:**

### **1. Render (Khuyến nghị)**
```bash
# Deploy backend trên Render
# Không giới hạn execution time
# Hỗ trợ model lớn
```

### **2. Fly.io**
```bash
# Deploy backend trên Fly.io
# Performance cao
# Global deployment
```

### **3. Netlify Functions**
```bash
# Deploy backend trên Netlify
# Tương tự Vercel
# 10s execution limit
```

---

## 🔍 **Testing Vercel Backend:**

### **1. Health Check**
```bash
curl https://your-backend-url.vercel.app/api/health
```

### **2. Prediction Test**
```bash
curl -X POST https://your-backend-url.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "base64_encoded_image"}'
```

---

## ⚠️ **Troubleshooting:**

### **Lỗi 1: Function timeout**
```bash
# Giảm model size
# Tối ưu prediction code
# Sử dụng model nhẹ hơn
```

### **Lỗi 2: Function size limit**
```bash
# Sử dụng tensorflow-cpu
# Loại bỏ dependencies không cần thiết
# Compress model
```

### **Lỗi 3: Cold start chậm**
```bash
# Pre-warm functions
# Sử dụng edge functions
# Cache model
```

---

## 🎉 **Kết Luận:**

**Vercel có thể deploy backend nhưng không phù hợp cho AI models lớn.**

**Khuyến nghị: Sử dụng Render hoặc Fly.io cho backend, Vercel cho frontend.**

**Happy Deploying! 🚀**
