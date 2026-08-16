import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

function MonthlyBarChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-lg flex items-center justify-center h-64">
        <p className="text-slate-500 text-sm">No data yet — upload a CSV.</p>
      </div>
    );
  }

  const chartData = {
    labels: data.map((d) => d.month),
    datasets: [
      {
        label: "Total Spend",
        data: data.map((d) => Math.abs(d.total)),
        backgroundColor: "#3b82f6",
        borderRadius: 4,
      },
    ],
  };

  const options = {
    plugins: {
      legend: { display: false },
    },
    scales: {
      x: { ticks: { color: "#64748b" }, grid: { color: "#e2e8f0" } },
      y: { ticks: { color: "#64748b" }, grid: { color: "#e2e8f0" } },
    },
  };

  return (
    <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-lg">
      <h2 className="text-lg font-semibold text-slate-800 mb-3">
        Monthly Totals
      </h2>
      <Bar data={chartData} options={options} />
    </div>
  );
}

export default MonthlyBarChart;