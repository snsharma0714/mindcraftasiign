import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home";
import "./App.css";

function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [maskedImage, setMaskedImage] = useState(null);
  const [maskedImageName, setMaskedImageName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setMaskedImage(null);
    setMaskedImageName("");
    setError("");
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select an image file.");
      return;
    }
    setLoading(true);
    setError("");
    const formData = new FormData();
    formData.append("file", selectedFile);
    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error("Failed to process image.");
      }
      const blob = await response.blob();
      // Get filename from Content-Disposition header
      const disposition = response.headers.get("Content-Disposition");
      let filename = "masked_image.png";
      if (disposition) {
        const match = disposition.match(/filename=([^;]+)/);
        if (match) filename = match[1];
      }
      setMaskedImage(URL.createObjectURL(blob));
      setMaskedImageName(filename);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!maskedImage) return;
    const link = document.createElement("a");
    link.href = maskedImage;
    link.download = maskedImageName || "masked_image.png";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>PII Masking App</h1>
        <p className="subtitle">Protect your privacy by masking sensitive info in ID images</p>
      </div>
      <div className="upload-section">
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Processing..." : "Upload & Mask"}
        </button>
        {error && <div className="error">{error}</div>}
      </div>
      <div className="preview-section">
        {selectedFile && (
          <div className="image-card">
            <h3>Original Image</h3>
            <img src={URL.createObjectURL(selectedFile)} alt="Original" />
          </div>
        )}
        {maskedImage && (
          <div className="image-card">
            <h3>Masked Image</h3>
            <img src={maskedImage} alt="Masked" />
          </div>
        )}
      </div>
      {maskedImage && (
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '40px' }}>
          <button style={{ padding: '14px 36px', fontSize: '1.1rem', borderRadius: '10px', background: 'linear-gradient(90deg, #185a9d 0%, #43cea2 100%)', color: '#fff', fontWeight: 600, border: 'none', cursor: 'pointer', boxShadow: '0 2px 8px rgba(44, 62, 80, 0.09)' }} onClick={handleDownload}>
            Download Masked Image
          </button>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<UploadPage />} />
      </Routes>
    </Router>
  );
}

export default App;
