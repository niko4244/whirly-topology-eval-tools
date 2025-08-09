import api from "./index";

// Trigger training and poll for status
export async function startTraining(name) {
  return api.post("/training", { name });
}

export async function fetchTrainingStatus() {
  return api.get("/training");
}

export async function updateTrainingProgress(id, progress) {
  return api.put(`/training/${id}/progress`, { progress });
}

export async function deleteTraining(id) {
  return api.delete(`/training/${id}`);
}