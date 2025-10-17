# 🆓 Hướng Dẫn Deploy Miễn Phí - Cognivasc

## 🎯 Tổng Quan

Project Cognivasc có thể deploy miễn phí trên nhiều platform khác nhau. Tuy nhiên, do model AI lớn (4.8MB) và yêu cầu TensorFlow, cần chọn platform phù hợp.

## 🚀 **Phương Án Tốt Nhất: Railway + Vercel**

### **Backend trên Railway** (Miễn phí)
- ✅ Hỗ trợ Python + TensorFlow
- ✅ Persistent storage cho model
- ✅ Không giới hạn thời gian chạy
- ✅ Custom domain

### **Frontend trên Vercel** (Miễn phí)
- ✅ Tốc độ nhanh nhất
- ✅ CDN global
- ✅ Auto deployment từ Git
- ✅ Custom domain

---

## 🛠️ **Hướng Dẫn Deploy Chi Tiết**

### **Bước 1: Deploy Backend trên Railway**

#### 1.1. Chuẩn bị
```bash
# Clone repository
git clone <your-repo-url>
cd Cognivasc
```

#### 1.2. Tạo Railway Project
1. Truy cập [railway.app](https://railway.app)
2. Đăng nhập bằng GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Chọn repository Cognivasc
5. Chọn folder `backend`

#### 1.3. Cấu hình Environment Variables
Trong Railway dashboard, thêm:
```
API_HOST=0.0.0.0
API_PORT=$PORT
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

#### 1.4. Deploy
Railway sẽ tự động:
- Detect Python project
- Install dependencies từ `requirements.txt`
- Chạy `python app.py`

**URL Backend**: `https://your-project-name.railway.app`

---

### **Bước 2: Deploy Frontend trên Vercel**

#### 2.1. Chuẩn bị Frontend
```bash
cd frontend
```

#### 2.2. Cập nhật API URL
Tạo file `frontend/.env.production`:
```env
VITE_API_URL=https://your-project-name.railway.app
```

#### 2.3. Deploy trên Vercel
1. Truy cập [vercel.com](https://vercel.com)
2. Đăng nhập bằng GitHub
3. Click "New Project"
4. Import repository Cognivasc
5. Chọn folder `frontend`
6. Build Command: `npm run build`
7. Output Directory: `dist`

**URL Frontend**: `https://your-project-name.vercel.app`

---

## 🔄 **Phương Án Thay Thế**

### **Option 1: Render (Full-stack)**

#### Ưu điểm:
- ✅ Deploy cả frontend và backend
- ✅ Persistent storage
- ✅ Auto SSL

#### Nhược điểm:
- ❌ Free tier có giới hạn 750 giờ/tháng
- ❌ Sleep sau 15 phút không hoạt động

#### Cách deploy:
1. Truy cập [render.com](https://render.com)
2. Connect GitHub repository
3. Tạo 2 services:
   - **Web Service** cho backend
   - **Static Site** cho frontend

### **Option 2: Netlify + Railway**

#### Frontend trên Netlify:
1. Truy cập [netlify.com](https://netlify.com)
2. Connect GitHub repository
3. Build settings:
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/dist`

#### Backend trên Railway:
Như hướng dẫn ở trên.

### **Option 3: Heroku (Có giới hạn)**

#### ⚠️ Lưu ý:
- Heroku đã dừng free tier từ 2022
- Cần trả phí $7/tháng

---

## 📋 **Checklist Deploy**

### **Trước khi deploy:**
- [ ] Model file `anemia_model.keras` có trong backend
- [ ] `requirements.txt` đầy đủ dependencies
- [ ] `package.json` có build script
- [ ] Environment variables được cấu hình

### **Sau khi deploy:**
- [ ] Backend health check: `https://your-backend-url/health`
- [ ] Frontend load được
- [ ] API connection hoạt động
- [ ] Upload và predict ảnh thành công

---

## 🔧 **Troubleshooting**

### **Backend Issues:**

#### 1. Model không load được
```bash
# Kiểm tra model file size
ls -la backend/anemia_model.keras

# Kiểm tra logs
railway logs
```

#### 2. Memory issues
```bash
# Thêm vào requirements.txt
tensorflow-cpu  # Thay vì tensorflow
```

#### 3. CORS errors
```bash
# Cập nhật CORS_ORIGINS
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

### **Frontend Issues:**

#### 1. API connection failed
```bash
# Kiểm tra API URL trong .env
VITE_API_URL=https://your-backend-url.railway.app
```

#### 2. Build failed
```bash
# Kiểm tra Node version
node --version  # Cần >= 18.0.0
```

---

## 💰 **So Sánh Chi Phí**

| Platform | Free Tier | Limitations | Best For |
|----------|-----------|-------------|----------|
| **Railway** | ✅ Unlimited | 500MB RAM, 1GB storage | Backend |
| **Vercel** | ✅ Unlimited | 100GB bandwidth | Frontend |
| **Render** | ✅ 750h/month | Sleep after 15min | Full-stack |
| **Netlify** | ✅ 100GB bandwidth | 300 build minutes | Frontend |
| **Heroku** | ❌ Paid only | $7/month | Full-stack |

---

## 🎯 **Khuyến Nghị**

### **Cho Production:**
1. **Railway** cho backend (miễn phí, ổn định)
2. **Vercel** cho frontend (tốc độ cao, CDN)

### **Cho Development:**
1. **Render** cho full-stack (dễ setup)
2. **Local development** với Docker

### **Cho Demo:**
1. **Vercel** cho cả frontend và backend (có giới hạn model size)

---

## 🚀 **Quick Start Commands**

### **Railway + Vercel:**
```bash
# 1. Deploy backend
# - Go to railway.app
# - Connect GitHub repo
# - Select backend folder
# - Add environment variables

# 2. Deploy frontend
# - Go to vercel.com
# - Connect GitHub repo
# - Select frontend folder
# - Add VITE_API_URL environment variable
```

### **Render (Full-stack):**
```bash
# 1. Go to render.com
# 2. Connect GitHub repo
# 3. Create Web Service (backend)
# 4. Create Static Site (frontend)
```

---

## 📞 **Support**

Nếu gặp vấn đề:
1. Kiểm tra logs trên platform
2. Verify environment variables
3. Test API endpoints
4. Check model file size

**Happy Deploying! 🎉**
