// Simple JWT login utility
import api from "../api";

export async function login(email, password) {
  const res = await api.post("/auth/token", new URLSearchParams({ username: email, password }));
  localStorage.setItem("jwt", res.data.access_token);
}

export function logout() {
  localStorage.removeItem("jwt");
}