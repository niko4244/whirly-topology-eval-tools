import api from "./index";

// CRUD Operations
export async function createComponent(data) {
  return api.post("/components", data);
}

export async function fetchComponents(query = "") {
  return api.get("/components", { params: { q: query } });
}

export async function updateComponent(id, data) {
  return api.put(`/components/${id}`, data);
}

export async function deleteComponent(id) {
  return api.delete(`/components/${id}`);
}