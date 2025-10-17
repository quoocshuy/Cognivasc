# Cognivasc Anemia Detection API

API REST cho hệ thống dự đoán thiếu máu qua ảnh kết mạc sử dụng Deep Learning.

## 🚀 Cài đặt và Chạy

### 1. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

### 2. Chạy Server

#### Cách 1: Sử dụng script khởi động (Khuyến nghị)
```bash
python start_server.py
```

#### Cách 2: Chạy trực tiếp
```bash
python app.py
```

#### Cách 3: Sử dụng uvicorn
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Kiểm tra Server

Mở trình duyệt và truy cập:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root Endpoint**: http://localhost:8000/

## 📋 API Endpoints

### `GET /`
Thông tin cơ bản về API.

**Response:**
```json
{
  "message": "Cognivasc Anemia Detection API",
  "version": "1.0.0",
  "status": "running",
  "model_ready": true,
  "endpoints": {
    "health": "/health",
    "predict": "/predict",
    "docs": "/docs"
  }
}
```

### `GET /health`
Kiểm tra trạng thái server và model.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123,
  "model": {
    "loaded": true,
    "ready": true,
    "load_time": 2.5,
    "path": "/path/to/anemia_model.keras",
    "exists": true
  },
  "server": {
    "uptime": 3600.0,
    "version": "1.0.0"
  }
}
```

### `POST /predict`
Dự đoán thiếu máu từ ảnh kết mạc.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: File upload (image)

**Response:**
```json
{
  "label": "Nghi ngờ Thiếu máu",
  "advice": "<b>Kết quả: Có dấu hiệu Thiếu máu</b><br>Khuyên bạn nên tham khảo ý kiến bác sĩ sớm.",
  "confidence": {
    "Thiếu máu": 0.85,
    "Không Thiếu máu": 0.15
  }
}
```

## 🧪 Test API

### Sử dụng curl
```bash
# Health check
curl http://localhost:8000/health

# Test prediction
curl -X POST "http://localhost:8000/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test_image.jpg"
```

### Sử dụng Python
```python
import requests

# Test health
response = requests.get("http://localhost:8000/health")
print(response.json())

# Test prediction
with open("test_image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/predict", files=files)
    print(response.json())
```

## ⚙️ Cấu hình

### Model Configuration
- **Model Path**: `anemia_model.keras`
- **Image Size**: 224x224 pixels
- **Threshold**: 0.1641
- **Classes**: ['anemia', 'non-anemia']

### Server Configuration
- **Host**: 0.0.0.0 (tất cả interfaces)
- **Port**: 8000
- **CORS**: Enabled cho tất cả origins

## 🔧 Troubleshooting

### Model không tải được
1. Kiểm tra file `anemia_model.keras` có tồn tại không
2. Kiểm tra quyền đọc file
3. Xem log chi tiết trong console

### Lỗi CORS
- API đã được cấu hình CORS cho tất cả origins
- Nếu vẫn gặp lỗi, kiểm tra frontend có gửi đúng headers không

### Lỗi 503 Service Unavailable
- Model chưa được tải thành công
- Kiểm tra endpoint `/health` để xem trạng thái model

## 📊 Performance

- **Model Load Time**: ~2-5 giây (tùy thuộc vào hardware)
- **Prediction Time**: ~0.1-0.5 giây mỗi ảnh
- **Memory Usage**: ~500MB-1GB (tùy thuộc vào model size)

## 🛡️ Security

- API không yêu cầu authentication (có thể thêm sau)
- File upload được validate (chỉ chấp nhận ảnh)
- Kích thước ảnh tối thiểu: 50x50 pixels

## 📝 Logs

Server ghi log chi tiết bao gồm:
- Model loading process
- Prediction requests
- Error messages
- Performance metrics

## 🔄 Development

### Auto-reload
```bash
python start_server.py --reload
```

### Multiple workers (Production)
```bash
python start_server.py --workers 4
```

### Custom host/port
```bash
python start_server.py --host 127.0.0.1 --port 9000
```
