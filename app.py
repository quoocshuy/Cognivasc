import gradio as gr
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image

# =============================================================================
# CẤU HÌNH VÀ TẢI MODEL
# =============================================================================
MODEL_PATH = "anemia_model.keras"
IMG_SIZE = (224, 224)
OPTIMIZED_THRESHOLD = 0.1641
CLASS_NAMES = ['anemia', 'non-anemia']
ANEMIA_INDEX = CLASS_NAMES.index('anemia')

print("Đang tải model...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model đã được tải thành công.")
except Exception as e:
    print(f"LỖI: Không thể tải model. Hãy chắc chắn file '{MODEL_PATH}' tồn tại.")
    print(e)
    model = None

# =============================================================================
# CÁC HÀM XỬ LÝ (Không cần thay đổi)
# =============================================================================

def preprocess_image(img_pil):
    """Tiền xử lý ảnh PIL đầu vào để phù hợp với model."""
    img_np = np.array(img_pil).astype('uint8')
    if len(img_np.shape) == 2 or img_np.shape[2] == 1:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
    if img_np.shape[2] == 4:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
    img_resized = cv2.resize(img_np, IMG_SIZE)
    img_expanded = np.expand_dims(img_resized, axis=0)
    return tf.keras.applications.mobilenet_v3.preprocess_input(img_expanded)

def predict(input_image):
    """Hàm chính: nhận ảnh, dự đoán, trả về lời khuyên và độ tin cậy."""
    try:
        if model is None:
            raise ValueError("Model chưa được tải thành công.")

        processed_input = preprocess_image(input_image)
        raw_prob = model.predict(processed_input)[0][0]

        # Vì model output = P(non-anemia), nên:
        anemia_score = 1 - raw_prob  

        print("-" * 30)
        print(f"[DEBUG] raw_prob (P[non-anemia]): {raw_prob:.4f}")
        print(f"[DEBUG] anemia_score (P[anemia]): {anemia_score:.4f}")
        print(f"[DEBUG] Ngưỡng đang sử dụng: {OPTIMIZED_THRESHOLD}")

        if anemia_score > OPTIMIZED_THRESHOLD:
            result_status = "Nghi ngờ Thiếu máu"
            advice_text = """
            <p style='font-size: 1.2em; color: #D32F2F; text-align: center;'>
            <b>Kết quả: Có dấu hiệu Thiếu máu</b>
            </p>
            <p><b>Lời khuyên:</b> Kết quả phân tích cho thấy các dấu hiệu của thiếu máu. 
            Chúng tôi khuyên bạn nên <b>tham khảo ý kiến bác sĩ sớm</b> để được chẩn đoán và tư vấn chính xác.</p>
            """
        else:
            result_status = "Không nghi ngờ Thiếu máu"
            advice_text = """
            <p style='font-size: 1.2em; color: #388E3C; text-align: center;'>
            <b>Kết quả: Không có dấu hiệu Thiếu máu</b>
            </p>
            <p><b>Lời khuyên:</b> Dựa trên hình ảnh, mô hình không phát hiện dấu hiệu thiếu máu. 
            Tuy nhiên, hãy luôn duy trì lối sống lành mạnh và <b>khám sức khỏe định kỳ</b>.</p>
            """

        print(f"[DEBUG] Kết quả: {result_status} (Vì {anemia_score:.4f} so với ngưỡng {OPTIMIZED_THRESHOLD})")
        print("-" * 30)

        confidence_output = {
            "Thiếu máu": float(anemia_score),
            "Không Thiếu máu": float(raw_prob)
        }
        return advice_text, confidence_output

    except Exception as e:
        print("!!!!!!!!!!!!!! LỖI TRONG QUÁ TRÌNH DỰ ĐOÁN !!!!!!!!!!!!!!")
        print(e)
        error_message = f"Đã có lỗi xảy ra: {e}"
        return f"<p style='color: red;'><b>Lỗi:</b> {error_message}</p>", {"Lỗi": 1.0}


# =============================================================================
# GIAO DIỆN NGƯỜI DÙNG (GRADIO UI - Không cần thay đổi)
# =============================================================================
with gr.Blocks(
    theme=gr.themes.Soft(font=[gr.themes.GoogleFont("Inter"), "Arial", "sans-serif"]),
    css="body, .gradio-container { font-size: 16px !important; } footer {display: none !important}"
) as app:
    
    gr.Markdown(
        """
        <div style="text-align: center;"> 
            <h1>Ứng dụng Sàng lọc Thiếu máu qua Ảnh kết mạc</h1>
            <p>Một dự án nghiên cứu khoa học sử dụng Trí tuệ nhân tạo</p>
        </div>
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(type="pil", label="Tải ảnh lên hoặc chọn ảnh mẫu")
            
            with gr.Accordion("💡 Hướng dẫn chụp ảnh để có kết quả tốt nhất", open=False):
                gr.Markdown("""
                1.  **Ánh sáng:** Chụp ở nơi có đủ sáng, tránh bóng tối và đèn flash trực tiếp.
                2.  **Độ nét:** Giữ điện thoại chắc tay để ảnh không bị mờ, nhòe.
                3.  **Góc chụp:** Kéo nhẹ mí mắt dưới xuống và nhìn thẳng vào camera.
                4.  **Chất lượng:** Đảm bảo ảnh rõ nét, cho thấy rõ các mạch máu bên trong mí mắt.
                """)

            gr.Examples(
                examples=["dataset/test/anemia/15.jpg", "dataset/test/non-anemia/16.jpg", "dataset/test/non-anemia/44.jpg"],
                inputs=input_image,
                label="Ảnh mẫu"
            )
            submit_button = gr.Button("Bắt đầu Phân tích", variant="primary", scale=2)
            
        with gr.Column(scale=1):
            gr.Markdown("### **Kết quả Phân tích**")
            
            with gr.Accordion("1. Lời khuyên & Kết quả", open=True):
                advice_output = gr.Markdown()
            
            with gr.Accordion("2. Phân tích Độ tin cậy của Model", open=True):
                confidence_chart = gr.Label(label="Điểm tin cậy", num_top_classes=2)

    gr.Markdown(
        """
        ---
        <p style='text-align: center; font-size: 0.9em;'>
        <b>Tuyên bố miễn trừ trách nhiệm:</b> Đây là một công cụ nghiên cứu và không thể thay thế cho chẩn đoán y tế chuyên nghiệp.
        Vui lòng tham khảo ý kiến bác sĩ để có kết quả chính xác nhất.
        </p>
        """
    )

    submit_button.click(
        fn=predict,
        inputs=input_image,
        outputs=[advice_output, confidence_chart],
        api_name="predict"
    )

if __name__ == "__main__":
    app.launch(share=True)
    