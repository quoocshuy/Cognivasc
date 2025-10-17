# 👥 Hướng Dẫn Cho Collaborators

## 🎯 Khi Bạn Được Mời Vào Dự Án

### **Bước 1: Kiểm Tra Quyền Hạn**
1. Vào repository trên GitHub
2. Click tab "Settings" → "Manage access"
3. Xem role của bạn (Admin/Write/Triage/Read)

### **Bước 2: Clone Repository**
```bash
git clone https://github.com/username/Cognivasc.git
cd Cognivasc
```

### **Bước 3: Deploy Backend (Railway)**
```bash
# 1. Truy cập railway.app
# 2. Đăng nhập bằng GitHub
# 3. Click "New Project" → "Deploy from GitHub repo"
# 4. Chọn repository "Cognivasc"
# 5. Chọn folder "backend"
# 6. Add environment variables:
#    - API_HOST=0.0.0.0
#    - API_PORT=$PORT
#    - LOG_LEVEL=INFO
#    - CORS_ORIGINS=https://your-frontend-url.vercel.app
```

### **Bước 4: Deploy Frontend (Vercel)**
```bash
# 1. Truy cập vercel.com
# 2. Đăng nhập bằng GitHub
# 3. Click "New Project"
# 4. Import repository "Cognivasc"
# 5. Chọn folder "frontend"
# 6. Add environment variable:
#    - VITE_API_URL=https://your-backend-url.railway.app
```

### **Bước 5: Test Deployment**
```bash
# Test backend
curl https://your-backend-url.railway.app/health

# Test frontend
# Mở browser: https://your-frontend-url.vercel.app
```

## 🔄 **Workflow Phát Triển**

### **Tạo Feature Mới:**
```bash
# 1. Tạo branch mới
git checkout -b feature/your-feature-name

# 2. Phát triển feature
# 3. Test locally
npm run dev  # Frontend
python app.py  # Backend

# 4. Commit changes
git add .
git commit -m "Add: your feature description"

# 5. Push branch
git push origin feature/your-feature-name

# 6. Tạo Pull Request trên GitHub
```

### **Fix Bug:**
```bash
# 1. Tạo branch bugfix
git checkout -b bugfix/issue-description

# 2. Fix bug
# 3. Test fix
# 4. Commit và push
git add .
git commit -m "Fix: bug description"
git push origin bugfix/issue-description

# 5. Tạo Pull Request
```

## 🚀 **Deploy Updates**

### **Auto Deploy:**
- **Railway**: Tự động deploy khi push vào main branch
- **Vercel**: Tự động deploy khi push vào main branch

### **Manual Deploy:**
```bash
# Railway
railway up

# Vercel
vercel --prod
```

## 🔧 **Environment Management**

### **Backend Environment (Railway):**
```env
API_HOST=0.0.0.0
API_PORT=$PORT
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-frontend-url.vercel.app
MAX_FILE_SIZE=10485760
PREDICTION_TIMEOUT=30
```

### **Frontend Environment (Vercel):**
```env
VITE_API_URL=https://your-backend-url.railway.app
```

## 📊 **Monitoring**

### **Railway Logs:**
```bash
# Xem logs
railway logs

# Hoặc trên Railway dashboard
```

### **Vercel Logs:**
```bash
# Xem logs
vercel logs

# Hoặc trên Vercel dashboard
```

## 🐛 **Troubleshooting**

### **Common Issues:**

#### 1. Permission Denied
```bash
# Kiểm tra quyền trên GitHub
# Settings → Manage access
```

#### 2. Deploy Failed
```bash
# Kiểm tra logs
railway logs
vercel logs

# Kiểm tra environment variables
```

#### 3. API Connection Failed
```bash
# Kiểm tra CORS settings
# Kiểm tra VITE_API_URL
```

## 📝 **Best Practices**

### **Code Standards:**
- Sử dụng TypeScript cho frontend
- Follow PEP 8 cho Python
- Viết commit message rõ ràng
- Tạo Pull Request với description chi tiết

### **Testing:**
```bash
# Test backend
python -m pytest backend/tests/

# Test frontend
npm test
```

### **Documentation:**
- Cập nhật README khi cần
- Viết comments trong code
- Document API changes

## 🆘 **Khi Cần Hỗ Trợ**

1. **Tạo Issue** trên GitHub
2. **Mention** chủ dự án
3. **Mô tả** vấn đề chi tiết
4. **Attach** logs nếu có

## 🎉 **Khi Hoàn Thành**

1. **Merge** Pull Request
2. **Test** production deployment
3. **Update** documentation
4. **Celebrate** 🎊
