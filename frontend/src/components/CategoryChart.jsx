import { Doughnut } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const COLORS = [
  "#60a5fa",
  "#f87171",
  "#fbbf24",
  "#34d399",
  "#a78bfa",
  "#f472b6",
  "#fb923c",
  "#22d3ee",
];

function CategoryChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-lg flex items-center justify-center h-64">
        <p className="text-slate-500 text-sm">No data yet — upload a CSV.</p>
      </div>
    );
  }

  const chartData = {
    labels: data.map((d) => d.category),
    datasets: [
      {
        data: data.map((d) => Math.abs(d.total)),
        backgroundColor: COLORS,
        borderWidth: 0,
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        position: "bottom",
        labels: { color: "#334155" },
      },
    },
  };

  return (
    <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-lg">
      <h2 className="text-lg font-semibold text-slate-800 mb-3">
        Spend by Category
      </h2>
      <Doughnut data={chartData} options={options} />
    </div>
  );
}

export default CategoryChart;