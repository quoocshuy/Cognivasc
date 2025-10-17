# 🔧 Render Troubleshooting Guide

## 🚨 **Lỗi Build trên Render**

### **Lỗi 1: OpenCV Dependencies**
```
error: failed to solve: process "/bin/sh -c apt-get update && apt-get install -y build-essential libgl1-mesa-glx..." did not complete successfully: exit code: 100
```

**🔧 Giải pháp:**
1. **Sử dụng `opencv-python-headless`** thay vì `opencv-python`
2. **Sử dụng `tensorflow-cpu`** thay vì `tensorflow`
3. **Tạo file `requirements-render.txt`** riêng

### **Lỗi 2: Memory Issues**
```
Process exited with status 137 (out of memory)
```

**🔧 Giải pháp:**
1. **Sử dụng `tensorflow-cpu`** thay vì `tensorflow`
2. **Giảm model size** nếu có thể
3. **Tối ưu imports**

### **Lỗi 3: Build Timeout**
```
Build timeout after 15 minutes
```

**🔧 Giải pháp:**
1. **Tối ưu requirements.txt**
2. **Sử dụng pre-built wheels**
3. **Giảm dependencies**

---

## 🛠️ **Cấu Hình Tối Ưu cho Render**

### **1. Requirements File (requirements-render.txt)**
```txt
fastapi
uvicorn[standard]
tensorflow-cpu
pillow
numpy
opencv-python-headless
gradio
python-multipart
```

### **2. Render Configuration (render-backend.yaml)**
```yaml
services:
  - type: web
    name: cognivasc-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements-render.txt
    startCommand: python app.py
    healthCheckPath: /health
```

### **3. Environment Variables**
```env
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=https://cognivasc-frontend.onrender.com
MAX_FILE_SIZE=10485760
PREDICTION_TIMEOUT=30
MODEL_LOAD_TIMEOUT=60
```

---

## 🚀 **Hướng Dẫn Deploy Render (Fixed)**

### **Bước 1: Chuẩn bị Files**
```bash
# Đảm bảo có file requirements-render.txt
# Đảm bảo có file render-backend.yaml
```

### **Bước 2: Deploy Backend**
1. Truy cập [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub repository
4. **Root Directory**: `backend`
5. **Build Command**: `pip install -r requirements-render.txt`
6. **Start Command**: `python app.py`
7. **Health Check Path**: `/health`

### **Bước 3: Set Environment Variables**
```env
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=https://cognivasc-frontend.onrender.com
MAX_FILE_SIZE=10485760
PREDICTION_TIMEOUT=30
MODEL_LOAD_TIMEOUT=60
```

### **Bước 4: Deploy Frontend**
1. Click "New" → "Static Site"
2. Connect GitHub repository
3. **Root Directory**: `frontend`
4. **Build Command**: `npm install && npm run build`
5. **Publish Directory**: `dist`
6. **Environment Variable**: `VITE_API_URL=https://cognivasc-backend.onrender.com`

---

## 🔍 **Debug Steps**

### **1. Kiểm tra Logs**
```bash
# Render Dashboard → Service → Logs
# Tìm lỗi cụ thể trong build logs
```

### **2. Test Local Build**
```bash
# Test requirements locally
pip install -r requirements-render.txt

# Test app locally
python app.py
```

### **3. Kiểm tra Model File**
```bash
# Đảm bảo model file tồn tại
ls -la backend/anemia_model.keras

# Kiểm tra kích thước
du -h backend/anemia_model.keras
```

---

## ⚡ **Tối Ưu Performance**

### **1. Model Optimization**
```python
# Trong app.py, thêm model optimization
import tensorflow as tf

# Optimize model loading
tf.config.optimizer.set_jit(True)
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)
```

### **2. Memory Management**
```python
# Clear cache after prediction
import gc
gc.collect()
```

### **3. Lazy Loading**
```python
# Load model only when needed
model = None

def get_model():
    global model
    if model is None:
        model = tf.keras.models.load_model(MODEL_PATH)
    return model
```

---

## 🆘 **Alternative Solutions**

### **Nếu Render vẫn không work:**

#### **1. Fly.io (Recommended)**
```bash
# Deploy trên Fly.io
fly launch
fly deploy
```

#### **2. Vercel API Routes**
```bash
# Deploy backend as Vercel functions
# Sử dụng vercel-api.json
```

#### **3. Netlify Functions**
```bash
# Deploy backend as Netlify functions
# Sử dụng netlify/functions/predict.py
```

---

## 📊 **Render vs Alternatives**

| Platform | OpenCV Support | Memory | Build Time | Best For |
|----------|----------------|--------|------------|----------|
| **Render** | ⚠️ Limited | 512MB | 5-10min | Simple apps |
| **Fly.io** | ✅ Full | 256MB | 3-5min | Performance |
| **Vercel** | ❌ No | 1GB | 1-2min | Frontend |
| **Netlify** | ❌ No | 1GB | 1-2min | Simple |

---

## 🎯 **Quick Fix Commands**

### **1. Update Requirements**
```bash
# Backup original
cp requirements.txt requirements-original.txt

# Use optimized version
cp requirements-render.txt requirements.txt
```

### **2. Test Build**
```bash
# Test locally
pip install -r requirements-render.txt
python app.py
```

### **3. Deploy**
```bash
# Push changes
git add .
git commit -m "Fix: Optimize for Render deployment"
git push origin main
```

---

## 🎉 **Success Checklist**

- [ ] ✅ Sử dụng `opencv-python-headless`
- [ ] ✅ Sử dụng `tensorflow-cpu`
- [ ] ✅ Set đúng environment variables
- [ ] ✅ Health check path: `/health`
- [ ] ✅ Model file tồn tại
- [ ] ✅ CORS origins đúng
- [ ] ✅ Build command: `pip install -r requirements-render.txt`

**Happy Deploying! 🚀**
