# 🔧 Environment Variables Guide

## 📋 **Backend Environment Variables**

### **🔴 Bắt Buộc (Required)**

| Variable | Value | Description |
|----------|-------|-------------|
| `API_HOST` | `0.0.0.0` | Host để bind server |
| `API_PORT` | `8000` | Port để chạy server |
| `LOG_LEVEL` | `INFO` | Mức độ logging |
| `CORS_ORIGINS` | `https://your-frontend-url.vercel.app` | CORS origins cho frontend |

### **🟡 Khuyến nghị (Recommended)**

| Variable | Value | Description |
|----------|-------|-------------|
| `MAX_FILE_SIZE` | `10485760` | Kích thước file tối đa (10MB) |
| `PREDICTION_TIMEOUT` | `30` | Timeout cho prediction (seconds) |
| `MODEL_LOAD_TIMEOUT` | `60` | Timeout cho model loading (seconds) |
| `API_WORKERS` | `1` | Số workers |

### **🟢 Tùy chọn (Optional)**

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | `your-secret-key` | Secret key cho security |
| `JWT_SECRET` | `your-jwt-secret` | JWT secret |
| `DATABASE_URL` | `postgresql://...` | Database connection |
| `REDIS_URL` | `redis://...` | Redis connection |
| `SENTRY_DSN` | `https://...` | Sentry monitoring |

---

## 📋 **Frontend Environment Variables**

### **🔴 Bắt Buộc (Required)**

| Variable | Value | Description |
|----------|-------|-------------|
| `VITE_API_URL` | `https://your-backend-url.onrender.com` | Backend API URL |

### **🟡 Khuyến nghị (Recommended)**

| Variable | Value | Description |
|----------|-------|-------------|
| `NODE_ENV` | `production` | Environment mode |

---

## 🚀 **Platform-Specific Setup**

### **1. Render (Backend)**

```env
# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# CORS Configuration
CORS_ORIGINS=https://cognivasc-frontend.onrender.com

# Performance Configuration
MAX_FILE_SIZE=10485760
PREDICTION_TIMEOUT=30
MODEL_LOAD_TIMEOUT=60
API_WORKERS=1
```

### **2. Render (Frontend)**

```env
# API Configuration
VITE_API_URL=https://cognivasc-backend.onrender.com

# Environment
NODE_ENV=production
```

### **3. Vercel (Frontend)**

```env
# API Configuration
VITE_API_URL=https://cognivasc-backend.onrender.com
```

### **4. Fly.io (Backend)**

```bash
# Set secrets
fly secrets set API_HOST=0.0.0.0
fly secrets set API_PORT=8080
fly secrets set LOG_LEVEL=INFO
fly secrets set CORS_ORIGINS=https://your-frontend-url.vercel.app
fly secrets set MAX_FILE_SIZE=10485760
fly secrets set PREDICTION_TIMEOUT=30
```

### **5. Netlify (Frontend)**

```env
# API Configuration
VITE_API_URL=https://your-backend-url.onrender.com
```

---

## 🔍 **Kiểm Tra Environment Variables**

### **Backend Test:**
```bash
# Test config
python -c "from config import get_config_summary; import json; print(json.dumps(get_config_summary(), indent=2))"
```

### **Frontend Test:**
```bash
# Check environment variables
echo $VITE_API_URL
```

---

## ⚠️ **Lưu Ý Quan Trọng**

### **1. CORS Configuration:**
- Phải match chính xác với frontend URL
- Không có trailing slash
- Sử dụng HTTPS cho production

### **2. API URL:**
- Frontend phải point đến đúng backend URL
- Kiểm tra protocol (http/https)
- Kiểm tra port

### **3. Security:**
- Không commit secrets vào Git
- Sử dụng platform-specific secret management
- Rotate keys định kỳ

### **4. Performance:**
- Tăng timeout nếu model lớn
- Giảm workers nếu memory hạn chế
- Monitor resource usage

---

## 🛠️ **Troubleshooting**

### **Common Issues:**

#### 1. CORS Error:
```bash
# Check CORS_ORIGINS
echo $CORS_ORIGINS
# Should match frontend URL exactly
```

#### 2. API Connection Failed:
```bash
# Check VITE_API_URL
echo $VITE_API_URL
# Should point to correct backend URL
```

#### 3. Model Loading Failed:
```bash
# Check model file
ls -la backend/anemia_model.keras
# Should exist and be readable
```

#### 4. Timeout Issues:
```bash
# Increase timeouts
PREDICTION_TIMEOUT=60
MODEL_LOAD_TIMEOUT=120
```

---

## 📊 **Environment Variables Summary**

| Platform | Backend | Frontend |
|----------|---------|----------|
| **Render** | ✅ Full support | ✅ Full support |
| **Vercel** | ⚠️ Limited (10s) | ✅ Full support |
| **Fly.io** | ✅ Full support | ❌ Use Vercel |
| **Netlify** | ⚠️ Limited (10s) | ✅ Full support |

---

## 🎯 **Quick Setup Commands**

### **Render:**
```bash
# Backend
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=https://cognivasc-frontend.onrender.com

# Frontend
VITE_API_URL=https://cognivasc-backend.onrender.com
```

### **Vercel:**
```bash
# Frontend only
VITE_API_URL=https://cognivasc-backend.onrender.com
```

### **Fly.io:**
```bash
fly secrets set API_HOST=0.0.0.0
fly secrets set API_PORT=8080
fly secrets set CORS_ORIGINS=https://your-frontend-url.vercel.app
```

**Happy Configuring! 🎉**
