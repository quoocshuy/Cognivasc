# 🚨 Vercel Không Phù Hợp Cho Backend AI

## ❌ **Vấn đề với Vercel:**

### **1. Giới hạn nghiêm trọng:**
- **10s execution limit** - Model AI cần nhiều thời gian hơn
- **50MB function size limit** - Model 4.8MB + dependencies vượt quá
- **Serverless functions** - Không phù hợp với persistent model loading
- **Cold start** - Model phải load lại mỗi lần request

### **2. Model AI quá lớn:**
- `anemia_model.keras`: 4.8MB
- TensorFlow dependencies: ~200MB
- OpenCV dependencies: ~50MB
- **Tổng cộng: ~250MB** (vượt quá giới hạn Vercel)

---

## ✅ **Giải Pháp Thay Thế:**

### **🥇 1. Render (Khuyến nghị nhất)**
```bash
# Deploy backend trên Render
# ✅ 750 giờ/tháng miễn phí
# ✅ Không giới hạn execution time
# ✅ Hỗ trợ model lớn
# ✅ Persistent storage
```

### **🥈 2. Fly.io**
```bash
# Deploy backend trên Fly.io
# ✅ 3 apps miễn phí
# ✅ Không giới hạn execution time
# ✅ Performance cao
# ✅ Global deployment
```

### **🥉 3. Railway (Trước đây)**
```bash
# Railway đã không còn free tier
# ❌ Cần trả phí
```

---

## 🚀 **Hướng Dẫn Deploy Render:**

### **Bước 1: Chuẩn bị**
```bash
# Đảm bảo có file requirements-render.txt
# Đảm bảo không có Dockerfile trong backend/
```

### **Bước 2: Deploy Backend**
1. Truy cập [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub repository
4. **Root Directory**: `backend`
5. **Environment**: Python 3
6. **Build Command**: `pip install -r requirements-render.txt`
7. **Start Command**: `python app.py`
8. **Health Check Path**: `/health`

### **Bước 3: Environment Variables**
```env
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-frontend-url.vercel.app
MAX_FILE_SIZE=10485760
PREDICTION_TIMEOUT=30
MODEL_LOAD_TIMEOUT=60
```

### **Bước 4: Deploy Frontend trên Vercel**
1. **Root Directory**: `frontend`
2. **Build Command**: `npm install && npm run build`
3. **Output Directory**: `dist`
4. **Environment Variable**: `VITE_API_URL=https://your-backend-url.onrender.com`

---

## 🚀 **Hướng Dẫn Deploy Fly.io:**

### **Bước 1: Cài đặt Fly CLI**
```bash
# Windows
iwr https://fly.io/install.ps1 -useb | iex

# macOS/Linux
curl -L https://fly.io/install.sh | sh
```

### **Bước 2: Deploy Backend**
```bash
cd backend
fly launch
# Chọn region gần nhất
# Chọn app name: cognivasc-backend
fly deploy
```

### **Bước 3: Set Environment Variables**
```bash
fly secrets set API_HOST=0.0.0.0
fly secrets set API_PORT=8080
fly secrets set CORS_ORIGINS=https://your-frontend-url.vercel.app
```

---

## 📊 **So Sánh Platforms:**

| Platform | Free Tier | Execution Time | Model Size | Best For |
|----------|-----------|----------------|------------|----------|
| **Vercel** | ✅ Unlimited | ❌ 10s limit | ❌ 50MB limit | Frontend |
| **Render** | ✅ 750h/month | ✅ Unlimited | ✅ Unlimited | Backend AI |
| **Fly.io** | ✅ 3 apps | ✅ Unlimited | ✅ Unlimited | Performance |
| **Netlify** | ✅ 100GB | ❌ 10s limit | ❌ 50MB limit | Frontend |

---

## 🎯 **Khuyến Nghị:**

### **✅ Sử dụng:**
- **Render** cho backend (AI models)
- **Vercel** cho frontend (React apps)

### **❌ Không nên:**
- **Vercel** cho backend AI
- **Netlify** cho backend AI

---

## 🔧 **Quick Fix:**

### **1. Deploy Backend trên Render:**
```bash
# 1. Truy cập render.com
# 2. New → Web Service
# 3. Root Directory: backend
# 4. Build Command: pip install -r requirements-render.txt
# 5. Start Command: python app.py
```

### **2. Deploy Frontend trên Vercel:**
```bash
# 1. Truy cập vercel.com
# 2. Root Directory: frontend
# 3. Build Command: npm run build
# 4. Output Directory: dist
```

---

## 🎉 **Kết Luận:**

**Vercel không phù hợp cho backend AI với model lớn. Sử dụng Render hoặc Fly.io cho backend, Vercel cho frontend.**

**Happy Deploying! 🚀**
