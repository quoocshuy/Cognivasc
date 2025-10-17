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
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Lỗi khi gọi API");
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
        <div className="mt-4 p-3 border rounded bg-gray-50">
          <p className="font-semibold">
            Kết quả: {result.label}
          </p>
          <ul>
            {Object.entries(result.confidence).map(([cls, val]) => (
              <li key={cls}>
                {cls}: {(val * 100).toFixed(2)}%
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
