import axios from "axios";

const api = axios.create({
  baseURL: "https://finance-dashboard-s96v.onrender.com",
});

export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/transactions/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const listTransactions = (category = null) =>
  api.get("/transactions", { params: { category } });

export const recategorizeTransaction = (id, category) =>
  api.patch(`/transactions/${id}`, { category });

export const getMonthlySummary = () => api.get("/summary/monthly");

export const getByCategorySummary = (month = null) =>
  api.get("/summary/by-category", { params: { month } });

export const getSubscriptionAlerts = () =>
  api.get("/alerts/subscription-increases");

export default api;