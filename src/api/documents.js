import api from "./index";

// Document upload (multipart, validation)
export async function uploadDocument(file, metadata = {}) {
  if (!file) throw new Error("File required");
  if (file.size > 10 * 1024 * 1024) throw new Error("File too large");
  if (!["application/pdf", "image/png", "image/jpeg"].includes(file.type)) throw new Error("Unsupported file type");

  const formData = new FormData();
  formData.append("file", file);
  Object.entries(metadata).forEach(([key, val]) => formData.append(key, val));

  return api.post("/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
}

export async function fetchDocuments() {
  return api.get("/documents");
}

export async function scanDocument(documentId) {
  return api.put(`/documents/${documentId}/scan`);
}

export async function deleteDocument(documentId) {
  return api.delete(`/documents/${documentId}`);
}