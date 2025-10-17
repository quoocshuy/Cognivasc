# 🩸 Cognivasc – Hệ thống Sàng lọc Thiếu máu qua Ảnh Niêm mạc

Dự án nghiên cứu khoa học sử dụng **Trí tuệ nhân tạo (AI)** để hỗ trợ **phát hiện thiếu máu** thông qua ảnh chụp **niêm mạc mắt**.
Cognivasc kết hợp **Deep Learning (TensorFlow)**, **FastAPI** cho backend, và **React (Vercel)** cho frontend, giúp xây dựng một hệ thống **AI có khả năng hoạt động thật trong môi trường web**.

---

## Mục tiêu dự án

- Ứng dụng học sâu để phân loại hình ảnh **anemia / non-anemia**.
- Hỗ trợ sàng lọc ban đầu, giúp phát hiện sớm tình trạng thiếu máu.
- Kết hợp AI + Web để mô hình có thể chạy **real-time trên trình duyệt**.
- Đóng góp vào hướng **AI vì sức khỏe cộng đồng**, đặc biệt tại Việt Nam.

---

## Cấu trúc thư mục



---
## Mô hình AI
- **Kiến trúc:** MobileNetV3 (tối ưu cho thiết bị nhẹ)
- **Đầu ra:** Xác suất `non-anemia` → tính `1 - p` để ra `anemia_score`
- **Ngưỡng tối ưu:** `OPTIMIZED_THRESHOLD = 0.1641`
- **Độ chính xác:** ~92% (F1-score trung bình trên tập test)

**Các lớp phân loại:**
| Nhãn | Mô tả | Viết tắt |
|------|--------|----------|
| `anemia` | Có dấu hiệu thiếu máu | Thiếu máu |
| `non-anemia` | Không có dấu hiệu thiếu máu | Không thiếu máu |

---

## 🩺 Nguyên lý hoạt động
1. Người dùng tải ảnh niêm mạc mắt lên qua giao diện (frontend hoặc Gradio).
2. Ảnh được xử lý → chuẩn hóa kích thước (224x224) → đưa vào model.
3. Model dự đoán và trả về:
   ```json
   {
     "label": "Thiếu máu",
     "confidence": {
       "Thiếu máu": 0.87,
       "Không thiếu máu": 0.13
     }
   }

## Chạy Backend (FastAPI)
1. **Cài thư viện**
`pip install fastapi uvicorn tensorflow pillow numpy opencv-python`
2. **Chạy server**
`uvicorn app:app --host 0.0.0.0 --port 8000`
3. **Kiểm tra**
- Mở trình duyệt, truy cập địa chỉ: http://localhost:8000/docs
- Đây là giao diện Swagger API.
- Endpoint chính để frontend gọi:
`POST http://localhost:8000/predict`

## Chạy Demo trên Gradio
`python gradio.py`
- Gradio sẽ tự mở tab trên trình duyệt.
- Giao diện gồm: tải ảnh, hướng dẫn chụp, kết quả và độ tin cậy.
- Hoặc truy cập: [Hugging Face Demo](https://huggingface.co/spaces/mhtth/cognivasc)

## Chạy Demo trên Vercel
- Truy cập: [Vercel Demo](https://cognivasc-gvdi.vercel.app/)