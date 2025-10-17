# 🆓 Railway Alternatives - Deploy Miễn Phí

## 🚨 **Railway đã không còn free tier!**

Đây là các lựa chọn thay thế **hoàn toàn miễn phí** tốt nhất:

---

## 🥇 **1. Render (Khuyến nghị nhất)**

### **✅ Ưu điểm:**
- **750 giờ/tháng miễn phí** (đủ cho hầu hết dự án)
- Hỗ trợ Python + TensorFlow
- Persistent storage (1GB)
- Auto SSL và custom domain
- Dễ setup

### **❌ Nhược điểm:**
- Sleep sau 15 phút không hoạt động
- Cold start có thể chậm

### **🚀 Cách Deploy:**

#### **Bước 1: Chuẩn bị**
```bash
# Đảm bảo có file render.yaml trong root
# File đã được tạo sẵn
```

#### **Bước 2: Deploy Backend**
1. Truy cập [render.com](https://render.com)
2. Đăng nhập bằng GitHub
3. Click "New" → "Web Service"
4. Connect repository "Cognivasc"
5. Cấu hình:
   - **Name**: `cognivasc-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Health Check Path**: `/health`

#### **Bước 3: Deploy Frontend**
1. Click "New" → "Static Site"
2. Connect repository "Cognivasc"
3. Cấu hình:
   - **Name**: `cognivasc-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
   - **Environment Variable**: `VITE_API_URL=https://cognivasc-backend.onrender.com`

**URLs:**
- Backend: `https://cognivasc-backend.onrender.com`
- Frontend: `https://cognivasc-frontend.onrender.com`

---

## 🥈 **2. Fly.io**

### **✅ Ưu điểm:**
- **3 apps miễn phí**
- 256MB RAM mỗi app
- Global deployment
- Không sleep
- Docker support

### **❌ Nhược điểm:**
- RAM hạn chế (256MB)
- Có thể không đủ cho TensorFlow

### **🚀 Cách Deploy:**

#### **Bước 1: Cài đặt Fly CLI**
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# macOS/Linux
curl -L https://fly.io/install.sh | sh
```

#### **Bước 2: Deploy Backend**
```bash
# Login
fly auth login

# Deploy backend
cd backend
fly launch
# Chọn region gần nhất (ví dụ: sin - Singapore)
# Chọn app name: cognivasc-backend

# Deploy
fly deploy
```

#### **Bước 3: Deploy Frontend (Vercel)**
```bash
# Deploy frontend lên Vercel
# Cập nhật VITE_API_URL = https://cognivasc-backend.fly.dev
```

**URLs:**
- Backend: `https://cognivasc-backend.fly.dev`
- Frontend: `https://your-frontend.vercel.app`

---

## 🥉 **3. Vercel API Routes**

### **✅ Ưu điểm:**
- **Unlimited** cho frontend
- Tốc độ nhanh nhất
- CDN global
- Auto deployment

### **❌ Nhược điểm:**
- **10s execution limit** (có thể không đủ cho AI model)
- Serverless functions
- Cold start

### **🚀 Cách Deploy:**

#### **Bước 1: Deploy Full-stack trên Vercel**
```bash
# 1. Truy cập vercel.com
# 2. Import repository
# 3. Cấu hình:
#    - Framework Preset: Other
#    - Build Command: npm run build
#    - Output Directory: frontend/dist
#    - Install Command: cd frontend && npm install
```

#### **Bước 2: Cấu hình API Routes**
- File `vercel-api.json` đã được tạo
- API sẽ available tại `/api/*`

**URLs:**
- Frontend: `https://your-project.vercel.app`
- API: `https://your-project.vercel.app/api/`

---

## 🏅 **4. Netlify Functions**

### **✅ Ưu điểm:**
- **100GB bandwidth miễn phí**
- Serverless functions
- Dễ setup

### **❌ Nhược điểm:**
- **10s execution limit**
- Có thể không đủ cho AI model

### **🚀 Cách Deploy:**

#### **Bước 1: Deploy Frontend**
```bash
# 1. Truy cập netlify.com
# 2. Import repository
# 3. Cấu hình:
#    - Build command: cd frontend && npm install && npm run build
#    - Publish directory: frontend/dist
```

#### **Bước 2: Deploy Backend Functions**
- File `netlify/functions/predict.py` đã được tạo
- Function sẽ available tại `/.netlify/functions/predict`

**URLs:**
- Frontend: `https://your-project.netlify.app`
- API: `https://your-project.netlify.app/.netlify/functions/predict`

---

## 🎯 **Khuyến Nghị Theo Use Case:**

### **🏆 Cho Production:**
1. **Render** - Ổn định nhất, đủ resources
2. **Fly.io** - Nếu cần performance cao

### **🚀 Cho Demo/Testing:**
1. **Vercel** - Nhanh nhất, dễ setup
2. **Netlify** - Đơn giản

### **💰 Cho Budget:**
1. **Render** - Free tier tốt nhất
2. **Fly.io** - Không sleep

---

## 📊 **So Sánh Chi Tiết:**

| Platform | Free Tier | RAM | Storage | Sleep | Best For |
|----------|-----------|-----|---------|-------|----------|
| **Render** | 750h/month | 512MB | 1GB | 15min | Production |
| **Fly.io** | 3 apps | 256MB | 1GB | No | Performance |
| **Vercel** | Unlimited | 1GB | - | No | Frontend |
| **Netlify** | 100GB | 1GB | - | No | Simple |

---

## 🚀 **Quick Start - Render (Khuyến nghị):**

```bash
# 1. Truy cập render.com
# 2. Connect GitHub repo
# 3. Deploy backend:
#    - Type: Web Service
#    - Build: pip install -r requirements.txt
#    - Start: python app.py
# 4. Deploy frontend:
#    - Type: Static Site
#    - Build: cd frontend && npm install && npm run build
#    - Publish: frontend/dist
# 5. Set environment variables
```

---

## 🔧 **Troubleshooting:**

### **Render Issues:**
```bash
# Check logs
# Render dashboard → Service → Logs

# Common fixes:
# - Increase timeout in render.yaml
# - Check environment variables
# - Verify model file size
```

### **Fly.io Issues:**
```bash
# Check logs
fly logs

# Scale resources
fly scale memory 512
```

### **Vercel Issues:**
```bash
# Check function logs
vercel logs

# Increase timeout (if possible)
# Update vercel.json maxDuration
```

---

## 🎉 **Kết Luận:**

**Render là lựa chọn tốt nhất** để thay thế Railway vì:
- Free tier generous (750h/month)
- Hỗ trợ đầy đủ Python + TensorFlow
- Persistent storage
- Dễ setup và maintain

**Happy Deploying! 🚀**
