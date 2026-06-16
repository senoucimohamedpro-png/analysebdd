import axios from "axios";

const api = axios.create({ baseURL: "/api" });

export const uploadCsv = (files) => {
  const form = new FormData();
  for (const f of files) form.append("files", f);
  return api.post("/upload", form, {
    headers: { "Content-Type": "multipart/form-data" },
  }).then((r) => r.data);
};

export const getHistory = () => api.get("/history").then((r) => r.data);

export const getSummary = (analysisId) =>
  api.get(`/history/${analysisId}/summary`).then((r) => r.data);

export const getFiches = (analysisId, params) =>
  api.get(`/history/${analysisId}/fiches`, { params }).then((r) => r.data);

export const getBlockingRules = () => api.get("/rules/blocking").then((r) => r.data);
export const updateBlockingRules = (rules) => api.put("/rules/blocking", rules).then((r) => r.data);
export const getClassificationRules = () => api.get("/rules/classification").then((r) => r.data);
export const updateClassificationRules = (rules) =>
  api.put("/rules/classification", rules).then((r) => r.data);

export const exportUrl = (analysisId, format, statut) => {
  const params = new URLSearchParams({ format, ...(statut ? { statut } : {}) });
  return `/api/export/${analysisId}?${params.toString()}`;
};

export default api;
