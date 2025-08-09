import React, { useState } from "react";
import "./DocumentUpload.css";
import scannerIcon from "../assets/icons/scanner.svg";

export default function DocumentUpload({ onUpload }) {
  const [dragActive, setDragActive] = useState(false);
  const [scanning, setScanning] = useState(false);
  const [progress, setProgress] = useState(0);

  function handleDrag(e) {
    e.preventDefault();
    setDragActive(e.type === "dragover");
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragActive(false);
    setScanning(true);
    setProgress(0);
    // Simulated scan progress
    let scanInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(scanInterval);
          setScanning(false);
          onUpload(e.dataTransfer.files[0]);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  }

  return (
    <div
      className={`upload-zone ${dragActive ? "active" : ""}`}
      onDragOver={handleDrag}
      onDragLeave={handleDrag}
      onDrop={handleDrop}
      tabIndex={0}
      aria-label="Document upload area"
    >
      <img src={scannerIcon} alt="Vintage scanner" className="scanner-icon" />
      <div className="upload-text">
        {scanning
          ? <div>
              <div className="scan-progress">
                <div className="progress-bar" style={{ width: `${progress}%` }} />
              </div>
              <span className="scan-label">Scanning...</span>
            </div>
          : <span>Drag & Drop your document here</span>}
      </div>
    </div>
  );
}