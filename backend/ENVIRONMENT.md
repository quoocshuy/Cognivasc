# Environment Configuration

## Environment Variables

Bạn có thể cấu hình API thông qua các environment variables sau:

### Server Configuration
```bash
export API_HOST=0.0.0.0          # Host để bind server
export API_PORT=8000             # Port để bind server
export API_WORKERS=1             # Số worker processes
```

### Logging Configuration
```bash
export LOG_LEVEL=INFO            # Log level (DEBUG, INFO, WARNING, ERROR)
```

### CORS Configuration
```bash
export CORS_ORIGINS=*            # CORS origins (comma-separated)
```

### Upload Configuration
```bash
export MAX_FILE_SIZE=10485760    # Max file size in bytes (10MB)
```

### Performance Configuration
```bash
export PREDICTION_TIMEOUT=30     # Prediction timeout in seconds
export MODEL_LOAD_TIMEOUT=60     # Model load timeout in seconds
```

## Example Usage

### Development
```bash
export API_HOST=127.0.0.1
export API_PORT=9000
export LOG_LEVEL=DEBUG
python app.py
```

### Production
```bash
export API_HOST=0.0.0.0
export API_PORT=8000
export API_WORKERS=4
export LOG_LEVEL=WARNING
python start_server.py --workers 4
```

### Docker
```bash
docker run -e API_PORT=8080 -e API_WORKERS=2 cognivasc-api
```

## Configuration File

Bạn cũng có thể chỉnh sửa trực tiếp file `config.py` để thay đổi cấu hình mặc định.
