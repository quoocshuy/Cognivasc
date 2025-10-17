import { useState } from "react";
import { Upload, AlertCircle, CheckCircle2, Loader2, Heart, Activity } from "lucide-react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { toast } from "sonner";

interface PredictionResult {
  label: string;
  advice: string;
  confidence: {
    "Thiếu máu": number;
    "Không Thiếu máu": number;
  };
}

export const DemoSection = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);

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

      // Lưu trực tiếp response từ backend
      setResult(data);
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
                <div className="space-y-6">
                  {/* Main Result Card */}
                  <div className={`rounded-xl p-6 ${
                    result.label.includes("Không nghi ngờ")
                      ? "bg-green-50 border-2 border-green-300"
                      : "bg-red-50 border-2 border-red-300"
                  }`}>
                    <div className="flex items-start space-x-4">
                      {result.label.includes("Không nghi ngờ") ? (
                        <CheckCircle2 className="w-8 h-8 text-green-600 flex-shrink-0" />
                      ) : (
                        <AlertCircle className="w-8 h-8 text-red-600 flex-shrink-0" />
                      )}
                      <div className="flex-1">
                        <h3 className="text-xl font-bold mb-2 text-gray-800">
                          {result.label}
                        </h3>
                        <div
                          className="text-sm text-gray-700"
                          dangerouslySetInnerHTML={{ __html: result.advice }}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Confidence Breakdown */}
                  <Card className="p-6">
                    <h4 className="text-lg font-semibold mb-4 flex items-center">
                      <Activity className="w-5 h-5 mr-2" />
                      Chi tiết độ tin cậy
                    </h4>
                    <div className="space-y-4">
                      {Object.entries(result.confidence).map(([key, value]) => (
                        <div key={key} className="space-y-2">
                          <div className="flex justify-between items-center">
                            <span className="font-medium text-gray-700">
                              {key === "Thiếu máu" ? (
                                <span className="flex items-center">
                                  <Heart className="w-4 h-4 mr-2 text-red-500" />
                                  {key}
                                </span>
                              ) : (
                                <span className="flex items-center">
                                  <CheckCircle2 className="w-4 h-4 mr-2 text-green-500" />
                                  {key}
                                </span>
                              )}
                            </span>
                            <span className="font-bold text-lg">
                              {(value * 100).toFixed(1)}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-3">
                            <div
                              className={`h-3 rounded-full transition-all duration-500 ${
                                key === "Thiếu máu"
                                  ? "bg-gradient-to-r from-red-400 to-red-600"
                                  : "bg-gradient-to-r from-green-400 to-green-600"
                              }`}
                              style={{ width: `${value * 100}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </Card>
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
