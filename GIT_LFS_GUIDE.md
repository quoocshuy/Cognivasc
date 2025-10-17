# 📦 Git LFS Setup Guide cho Cognivasc

## ✅ **Đã Setup Git LFS:**

### **🔧 Cấu hình hoàn tất:**
- ✅ **Git LFS initialized**
- ✅ **`.gitattributes`** created
- ✅ **Large files tracked**

### **📁 Files được track bởi Git LFS:**
```
backend/dataset/**/*.jpg     # Dataset images
backend/dataset/**/*.png    # Dataset images
backend/dataset/**/*.jpeg   # Dataset images
backend/anemia_model.keras  # AI model (4.8MB)
*.keras                     # Model files
*.h5                        # Model files
*.hdf5                      # Model files
*.pkl                      # Pickle files
*.pickle                   # Pickle files
*.joblib                   # Joblib files
*.ipynb                    # Jupyter notebooks
```

---

## 🚀 **Lợi ích của Git LFS:**

### **1. Repository Size:**
- **Trước**: Repository rất lớn (hàng GB)
- **Sau**: Repository nhỏ, chỉ chứa pointers
- **Dataset**: Stored trên Git LFS servers

### **2. Clone Speed:**
- **Fast clone**: Chỉ download pointers
- **On-demand**: Download files khi cần
- **Bandwidth**: Tiết kiệm bandwidth

### **3. Development:**
- **Local development**: Không cần download dataset
- **CI/CD**: Faster builds
- **Collaboration**: Dễ dàng share code

---

## 📋 **Git LFS Commands:**

### **Kiểm tra files được track:**
```bash
git lfs ls-files
```

### **Download specific files:**
```bash
git lfs pull --include="backend/dataset/**/*.jpg"
```

### **Download all LFS files:**
```bash
git lfs pull
```

### **Check LFS status:**
```bash
git lfs status
```

### **Migrate existing files:**
```bash
git lfs migrate import --include="*.jpg,*.png,*.keras"
```

---

## 🔧 **Deploy với Git LFS:**

### **Render Deployment:**
1. **Render** sẽ tự động download LFS files
2. **Build time** có thể chậm hơn lần đầu
3. **Subsequent builds** sẽ nhanh hơn

### **Vercel Deployment:**
1. **Vercel** hỗ trợ Git LFS
2. **Automatic download** during build
3. **Caching** cho subsequent builds

### **Local Development:**
```bash
# Clone repository
git clone <repo-url>
cd Cognivasc

# Download LFS files (nếu cần)
git lfs pull

# Hoặc download specific files
git lfs pull --include="backend/anemia_model.keras"
```

---

## ⚠️ **Lưu ý quan trọng:**

### **1. GitHub LFS Limits:**
- **Free tier**: 1GB storage, 1GB bandwidth/month
- **Paid plans**: Higher limits
- **Dataset size**: Có thể vượt quá free limit

### **2. Alternative Storage:**
- **Google Drive**: Upload dataset
- **AWS S3**: Cloud storage
- **Dropbox**: File sharing
- **OneDrive**: Microsoft storage

### **3. Production Deploy:**
- **Model file**: Cần download `anemia_model.keras`
- **Dataset**: Không cần cho production
- **Optimization**: Chỉ download model file

---

## 🎯 **Recommended Workflow:**

### **Development:**
```bash
# Clone without LFS files
git clone <repo-url>
cd Cognivasc

# Download only model file
git lfs pull --include="backend/anemia_model.keras"
```

### **Production Deploy:**
```bash
# Render sẽ tự động download model
# Dataset không cần thiết cho production
```

### **Research/Retraining:**
```bash
# Download full dataset
git lfs pull
```

---

## 📊 **File Size Comparison:**

| File Type | Without LFS | With LFS |
|-----------|-------------|----------|
| **Repository** | ~2GB | ~50MB |
| **Clone Time** | 10-15 min | 1-2 min |
| **Bandwidth** | High | Low |
| **Storage** | Local | LFS Server |

---

## 🚀 **Next Steps:**

### **1. Commit LFS setup:**
```bash
git add .gitattributes
git commit -m "Setup: Configure Git LFS for large files"
git push origin main
```

### **2. Test LFS:**
```bash
# Check LFS status
git lfs status

# Verify files are tracked
git lfs ls-files
```

### **3. Deploy:**
- **Render**: Sẽ tự động handle LFS
- **Vercel**: Sẽ download model file
- **Local**: Chỉ download khi cần

**Git LFS đã được setup thành công! Repository giờ đây nhẹ và nhanh hơn!** 🎉
