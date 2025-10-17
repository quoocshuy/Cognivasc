# 🚀 Hướng Dẫn Deploy Cognivasc Application

## 📋 Tổng Quan

Cognivasc là một ứng dụng AI để dự đoán thiếu máu qua ảnh kết mạc, bao gồm:
- **Backend**: FastAPI + TensorFlow (Python)
- **Frontend**: React + Vite + TypeScript
- **Model**: Keras model cho dự đoán thiếu máu

## 🛠️ Yêu Cầu Hệ Thống

### Minimum Requirements
- **OS**: Linux/macOS/Windows với WSL2
- **RAM**: 4GB (khuyến nghị 8GB)
- **Storage**: 10GB trống
- **CPU**: 2 cores (khuyến nghị 4 cores)

### Software Requirements
- **Docker**: >= 20.10
- **Docker Compose**: >= 2.0
- **Git**: để clone repository

## 📦 Cài Đặt Dependencies

### 1. Cài đặt Docker

#### Ubuntu/Debian:
```bash
# Cập nhật package list
sudo apt update

# Cài đặt dependencies
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release

# Thêm Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Thêm Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Cài đặt Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

#### Windows:
1. Tải Docker Desktop từ [docker.com](https://www.docker.com/products/docker-desktop)
2. Cài đặt và khởi động Docker Desktop
3. Enable WSL2 integration

#### macOS:
```bash
# Sử dụng Homebrew
brew install --cask docker
```

### 2. Verify Installation
```bash
docker --version
docker-compose --version
```

## 🚀 Deploy Application

### Phương Pháp 1: Sử dụng Deploy Script (Khuyến nghị)

```bash
# Clone repository
git clone <your-repo-url>
cd Cognivasc

# Chạy deploy script
./deploy.sh

# Hoặc trên Windows
bash deploy.sh
```

### Phương Pháp 2: Deploy Manual

```bash
# 1. Tạo thư mục cần thiết
mkdir -p backend/logs backend/cache nginx/ssl

# 2. Build và start services
docker-compose up -d --build

# 3. Kiểm tra status
docker-compose ps
```

## 🔧 Cấu Hình

### Environment Variables

Tạo file `.env` từ template:
```bash
cp env.example .env
```

Chỉnh sửa các biến trong `.env`:
```env
# Backend Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Upload Configuration
MAX_FILE_SIZE=10485760
PREDICTION_TIMEOUT=30
```

### Port Configuration

Mặc định:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Nginx** (production): http://localhost:80

Để thay đổi ports, chỉnh sửa `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Thay đổi port 8000 thành 8001
```

## 📊 Monitoring và Logs

### Xem Logs
```bash
# Tất cả services
docker-compose logs -f

# Chỉ backend
docker-compose logs -f backend

# Chỉ frontend
docker-compose logs -f frontend
```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000/health
```

### Container Status
```bash
# Xem status containers
docker-compose ps

# Xem resource usage
docker stats
```

## 🔄 Quản Lý Services

### Deploy Script Commands
```bash
./deploy.sh deploy    # Deploy application
./deploy.sh stop      # Stop services
./deploy.sh restart   # Restart services
./deploy.sh logs      # View logs
./deploy.sh status    # Show status
./deploy.sh clean     # Clean up everything
```

### Manual Commands
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild và start
docker-compose up -d --build

# Remove everything
docker-compose down --volumes --rmi all
```

## 🌐 Production Deployment

### 1. SSL/HTTPS Setup

Tạo SSL certificates:
```bash
# Tạo self-signed certificate (development)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/nginx-selfsigned.key \
  -out nginx/ssl/nginx-selfsigned.crt

# Hoặc sử dụng Let's Encrypt (production)
# certbot certonly --webroot -w /var/www/html -d yourdomain.com
```

### 2. Production Docker Compose

```bash
# Deploy với nginx reverse proxy
docker-compose --profile production up -d
```

### 3. Environment Variables cho Production

```env
NODE_ENV=production
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Kiểm tra port đang được sử dụng
netstat -tulpn | grep :8000

# Kill process sử dụng port
sudo kill -9 <PID>
```

#### 2. Docker Build Fails
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### 3. Model Loading Issues
```bash
# Kiểm tra model file
ls -la backend/anemia_model.keras

# Kiểm tra logs
docker-compose logs backend
```

#### 4. Memory Issues
```bash
# Tăng Docker memory limit
# Trong Docker Desktop: Settings > Resources > Memory
```

### Debug Mode

```bash
# Chạy với debug logs
LOG_LEVEL=DEBUG docker-compose up

# Vào container để debug
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 📈 Performance Optimization

### 1. Resource Limits
Thêm vào `docker-compose.yml`:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

### 2. Caching
```yaml
services:
  frontend:
    volumes:
      - node_modules_cache:/app/node_modules
volumes:
  node_modules_cache:
```

### 3. Multi-stage Build
Dockerfiles đã được tối ưu với multi-stage build để giảm kích thước image.

## 🔒 Security

### 1. Non-root User
Containers chạy với non-root user để tăng bảo mật.

### 2. Security Headers
Nginx đã được cấu hình với security headers.

### 3. Rate Limiting
API endpoints có rate limiting để tránh abuse.

## 📝 API Documentation

Sau khi deploy, truy cập:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🆘 Support

Nếu gặp vấn đề:
1. Kiểm tra logs: `docker-compose logs -f`
2. Kiểm tra health: `curl http://localhost:8000/health`
3. Restart services: `docker-compose restart`
4. Clean và rebuild: `./deploy.sh clean && ./deploy.sh deploy`

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
