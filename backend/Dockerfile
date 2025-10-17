# =============================================================================
# Dockerfile cho Cognivasc Backend (FastAPI + TensorFlow)
# =============================================================================

# Sử dụng Python 3.11 slim image để tối ưu kích thước
FROM python:3.11-slim

# Metadata
LABEL maintainer="Cognivasc Team"
LABEL description="Cognivasc Anemia Detection API"
LABEL version="1.0.0"

# Thiết lập environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Tạo user không phải root để bảo mật
RUN groupadd -r cognivasc && useradd -r -g cognivasc cognivasc

# Cài đặt system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements trước để tận dụng Docker layer caching
COPY requirements.txt .

# Cài đặt Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Tạo thư mục cho logs và cache
RUN mkdir -p /app/logs /app/cache && \
    chown -R cognivasc:cognivasc /app

# Chuyển sang user không phải root
USER cognivasc

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Command để chạy ứng dụng
CMD ["python", "app.py"]
