import React, { useState } from "react";
import { uploadDocument } from "../api/documents";

export default function DocumentUpload({ onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  async function handleUpload() {
    setStatus("uploading");
    setError("");
    try {
      const res = await uploadDocument(file, { uploadedAt: new Date().toISOString() });
      setStatus("done");
      onUploadComplete && onUploadComplete(res.data);
    } catch (err) {
      setError(err.message || "Upload failed");
      setStatus("error");
    }
  }

  return (
    <div>
      <input type="file" accept=".pdf,image/*" onChange={e => setFile(e.target.files[0])} />
      <button disabled={!file || status === "uploading"} onClick={handleUpload}>
        {status === "uploading" ? "Uploading..." : "Upload Document"}
      </button>
      {error && <div className="error">{error}</div>}
      {status === "done" && <div className="success">Upload complete!</div>}
    </div>
  );
}