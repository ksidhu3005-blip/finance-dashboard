import { useState } from "react";
import { uploadCSV } from "../api";

function UploadForm({ onUploaded }) {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleFileChange(e) {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setStatus(null);
    try {
      const res = await uploadCSV(file);
      setStatus({ type: "success", message: res.data.message });
      onUploaded();
    } catch (err) {
      const detail = err.response?.data?.detail || "Upload failed.";
      setStatus({ type: "error", message: detail });
    } finally {
      setLoading(false);
      e.target.value = "";
    }
  }

  return (
    <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-lg">
      <h2 className="text-lg font-semibold text-slate-800 mb-2">
        Upload Bank CSV
      </h2>
      <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-300 rounded-lg p-6 cursor-pointer hover:border-blue-500 transition">
        <span className="text-slate-500 text-sm">
          {loading ? "Uploading..." : "Click to select a CSV file"}
        </span>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="hidden"
          disabled={loading}
        />
      </label>

      {status && (
        <p
          className={`mt-3 text-sm ${
            status.type === "success" ? "text-green-600" : "text-red-600"
          }`}
        >
          {status.message}
        </p>
      )}
    </div>
  );
}

export default UploadForm;