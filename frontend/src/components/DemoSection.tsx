import { useState } from "react";
import { Upload, AlertCircle, CheckCircle2, Loader2 } from "lucide-react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { toast } from "sonner";

export const DemoSection = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<{
    prediction: "positive" | "negative";
    confidence: number;
  } | null>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.type.startsWith("image/")) {
        toast.error("Vui lòng upload một bức ảnh");
        return;
      }
      setSelectedFile(file);
      setResult(null);
      
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const analyzeImage = async () => {
  if (!selectedFile) return;
  setIsAnalyzing(true);

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    // Gọi API thật đến backend FastAPI
    const res = await fetch("http://localhost:8000/predict", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);

    const data = await res.json();
    console.log("Kết quả backend:", data);

    // Backend trả về ví dụ: { "label": "Thiếu máu", "confidence": { "Thiếu máu": 0.8, "Không thiếu máu": 0.2 } }
    const isAnemia = data.label.toLowerCase().includes("thiếu");
    const confidence =
      typeof data.confidence === "number"
        ? data.confidence
        : Object.values(data.confidence)[0];

    setResult({
      prediction: isAnemia ? "positive" : "negative",
      confidence: Math.round(confidence * 100) || 0,
    });

    toast.success("Phân tích hoàn tất!");
  } catch (err) {
    console.error("Lỗi khi gọi API:", err);
    toast.error("❌ Lỗi kết nối đến server! Kiểm tra backend.");
  } finally {
    setIsAnalyzing(false);
  }
};


  return (
    <section id="demo" className="min-h-screen bg-background py-20">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 text-primary">
            AI Demo
          </h2>
          <p className="text-center text-muted-foreground mb-12 text-lg">
            Tải lên hình ảnh kết mạc mắt để hệ thống AI phân tích và phát hiện thiếu máu.
          </p>

          <Card className="p-8 md:p-12 shadow-medium bg-gradient-card">
            <div className="space-y-8">
              {/* Upload Area */}
              <div className="border-2 border-dashed border-border rounded-xl p-8 text-center hover:border-primary transition-colors">
                <input
                  type="file"
                  id="file-upload"
                  className="hidden"
                  accept="image/*"
                  onChange={handleFileSelect}
                />
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer flex flex-col items-center"
                >
                  <Upload className="w-12 h-12 text-primary mb-4" />
                  <p className="text-lg font-semibold mb-2">
                    {selectedFile ? selectedFile.name : "Click to upload image"}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Định dạng được hỗ trợ: JPG, PNG, WEBP
                  </p>
                </label>
              </div>

              {/* Preview */}
              {preview && (
                <div className="space-y-4">
                  <div className="relative rounded-xl overflow-hidden shadow-soft max-w-md mx-auto">
                    <img
                      src={preview}
                      alt="Preview"
                      className="w-full h-auto"
                    />
                  </div>

                  <Button
                    onClick={analyzeImage}
                    disabled={isAnalyzing}
                    className="w-full bg-gradient-primary text-primary-foreground hover:opacity-90 transition-all hover:scale-105 text-lg py-6"
                  >
                    {isAnalyzing ? (
                      <>
                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                        Đang phân tích...
                      </>
                    ) : (
                      "Phân tích hình ảnh"
                    )}
                  </Button>
                </div>
              )}

              {/* Results */}
              {result && !isAnalyzing && (
                <div className={`rounded-xl p-6 ${
                  result.prediction === "negative" 
                    ? "bg-green-50 border-2 border-green-300" 
                    : "bg-red-50 border-2 border-red-300"
                }`}>
                  <div className="flex items-start space-x-4">
                    {result.prediction === "negative" ? (
                      <CheckCircle2 className="w-8 h-8 text-green-600 flex-shrink-0" />
                    ) : (
                      <AlertCircle className="w-8 h-8 text-red-600 flex-shrink-0" />
                    )}
                    <div className="flex-1">
                      <h3 className="text-xl font-bold mb-2">
                        {result.prediction === "negative" 
                          ? "No Anemia Detected" 
                          : "Anemia Detected"}
                      </h3>
                      <p className="text-muted-foreground mb-3">
                        Độ tin cậy: {result.confidence}%
                      </p>
                      <p className="text-sm">
                        {result.prediction === "negative" 
                          ? "The analysis suggests normal hemoglobin levels based on conjunctiva appearance." 
                          : "The analysis indicates possible anemia. Please consult a healthcare professional for proper diagnosis and treatment."}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Disclaimer */}
              <div className="bg-muted/50 rounded-lg p-4 text-sm text-muted-foreground">
                <p className="font-semibold mb-1">⚠️ Tuyên bố miễn trừ trách nhiệm:</p>
                <p>
                  Đây là một công cụ nghiên cứu và không thể thay thế cho chẩn đoán y tế chuyên nghiệp. Vui lòng tham khảo ý kiến bác sĩ để có kết quả chính xác nhất.
                </p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
};
