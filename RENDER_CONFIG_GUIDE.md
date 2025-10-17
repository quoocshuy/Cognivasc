# 🔧 Render Configuration Guide

## ✅ **Đã Cập Nhật Config cho Render:**

### **1. Cập nhật `config.py`:**
- ✅ **Render detection** - Tự động detect môi trường Render
- ✅ **PORT configuration** - Sử dụng PORT environment variable của Render
- ✅ **CORS optimization** - Cấu hình CORS cho Render URLs
- ✅ **Performance tuning** - Tối ưu cho Render free tier

### **2. Tạo `render-config.py`:**
- ✅ **Render-specific settings** - Cấu hình riêng cho Render
- ✅ **Free tier optimization** - Tối ưu cho free tier
- ✅ **Environment detection** - Tự động detect Render vs Local

---

## 🚀 **Cấu Hình Render Deployment:**

### **Environment Variables cần set trên Render:**

#### **🔴 Bắt buộc:**
```env
RENDER=true
PORT=8000
```

#### **🟡 Khuyến nghị:**
```env
LOG_LEVEL=INFO
CORS_ORIGINS=https://cognivasc-frontend.onrender.com
MAX_FILE_SIZE=10485760
PREDICTION_TIMEOUT=60
MODEL_LOAD_TIMEOUT=120
```

#### **🟢 Tùy chọn:**
```env
RENDER_FRONTEND_URL=https://cognivasc-frontend.onrender.com
ENVIRONMENT=production
```

---

## 📋 **Render Deployment Settings:**

### **Backend Service:**
- **Name**: `cognivasc-backend`
- **Environment**: `Python 3`
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements-render.txt`
- **Start Command**: `python app.py`
- **Health Check Path**: `/health`

### **Frontend Service:**
- **Name**: `cognivasc-frontend`
- **Type**: `Static Site`
- **Root Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`

---

## 🔧 **Cấu Hình Tự Động:**

### **Render Detection:**
```python
# Tự động detect Render environment
if os.getenv("RENDER"):
    PORT = int(os.getenv("PORT", 8000))
    HOST = "0.0.0.0"
    # Render-specific settings
```

### **CORS Configuration:**
```python
# Tự động cấu hình CORS cho Render
CORS_ORIGINS = [
    "https://cognivasc-frontend.onrender.com",
    "https://cognivasc.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173"
]
```

### **Performance Optimization:**
```python
# Tối ưu cho Render free tier
PREDICTION_TIMEOUT = 60  # 60 seconds
MODEL_LOAD_TIMEOUT = 120  # 2 minutes
WORKERS = 1  # Single worker
```

---

## 🚀 **Hướng Dẫn Deploy:**

### **Bước 1: Deploy Backend**
1. Truy cập [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub repository
4. **Root Directory**: `backend`
5. **Build Command**: `pip install -r requirements-render.txt`
6. **Start Command**: `python app.py`
7. **Health Check Path**: `/health`

### **Bước 2: Set Environment Variables**
```env
RENDER=true
LOG_LEVEL=INFO
CORS_ORIGINS=https://cognivasc-frontend.onrender.com
MAX_FILE_SIZE=10485760
PREDICTION_TIMEOUT=60
MODEL_LOAD_TIMEOUT=120
```

### **Bước 3: Deploy Frontend**
1. Click "New" → "Static Site"
2. **Root Directory**: `frontend`
3. **Build Command**: `npm install && npm run build`
4. **Publish Directory**: `dist`
5. **Environment Variable**: `VITE_API_URL=https://cognivasc-backend.onrender.com`

---

## 🔍 **Testing Configuration:**

### **1. Health Check:**
```bash
curl https://cognivasc-backend.onrender.com/health
```

### **2. CORS Test:**
```bash
curl -H "Origin: https://cognivasc-frontend.onrender.com" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://cognivasc-backend.onrender.com/predict
```

### **3. Prediction Test:**
```bash
curl -X POST https://cognivasc-backend.onrender.com/predict \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"
```

---

## ⚠️ **Troubleshooting:**

### **Lỗi 1: Port binding failed**
```bash
# Kiểm tra PORT environment variable
echo $PORT
# Phải là số (ví dụ: 8000)
```

### **Lỗi 2: CORS error**
```bash
# Kiểm tra CORS_ORIGINS
# Phải match chính xác với frontend URL
```

### **Lỗi 3: Model loading timeout**
```bash
# Tăng MODEL_LOAD_TIMEOUT
MODEL_LOAD_TIMEOUT=120
```

### **Lỗi 4: Memory issues**
```bash
# Sử dụng tensorflow-cpu
# Đã có trong requirements-render.txt
```

---

## 📊 **Render vs Local:**

| Setting | Render | Local |
|---------|--------|-------|
| **Host** | 0.0.0.0 | 0.0.0.0 |
| **Port** | $PORT | 8000 |
| **Workers** | 1 | 1 |
| **CORS** | Render URLs | * |
| **Timeout** | 60s | 30s |
| **Log Level** | INFO | DEBUG |

---

## 🎯 **Success Checklist:**

- [ ] ✅ `RENDER=true` environment variable
- [ ] ✅ `PORT` environment variable set
- [ ] ✅ CORS origins configured
- [ ] ✅ Model file exists
- [ ] ✅ Health check working
- [ ] ✅ Frontend can connect to backend

**Config đã được tối ưu cho Render! Deploy thôi! 🚀**
