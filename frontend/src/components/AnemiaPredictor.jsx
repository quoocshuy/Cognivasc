import React, { useState } from "react";

export default function AnemiaPredictor() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      console.log('API URL:', apiUrl); // Debug log
      const res = await fetch(`${apiUrl}/predict`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Lỗi khi gọi API: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto space-y-4">
      <h2 className="text-xl font-bold">Dự đoán Thiếu máu</h2>

      <input type="file" accept="image/*" onChange={handleFileChange} />

      <button
        onClick={handleSubmit}
        disabled={!file || loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {loading ? "Đang xử lý..." : "Gửi ảnh"}
      </button>

      {result && (
        <div className="mt-4 space-y-4">
          {/* Main Result */}
          <div className={`p-4 rounded-lg border-2 ${
            result.label.includes("Không nghi ngờ")
              ? "bg-green-50 border-green-300"
              : "bg-red-50 border-red-300"
          }`}>
            <h3 className="font-bold text-lg mb-2">{result.label}</h3>
            <div
              className="text-sm"
              dangerouslySetInnerHTML={{ __html: result.advice }}
            />
          </div>

          {/* Confidence Details */}
          <div className="p-3 border rounded bg-gray-50">
            <h4 className="font-semibold mb-2">Chi tiết độ tin cậy:</h4>
            <div className="space-y-2">
              {Object.entries(result.confidence).map(([cls, val]) => (
                <div key={cls} className="flex justify-between items-center">
                  <span className="text-sm">{cls}:</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-20 bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          cls === "Thiếu máu" ? "bg-red-500" : "bg-green-500"
                        }`}
                        style={{ width: `${val * 100}%` }}
                      />
                    </div>
                    <span className="text-sm font-medium">
                      {(val * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
