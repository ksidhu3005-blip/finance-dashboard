import { useEffect, useState } from "react";
import {
  listTransactions,
  getMonthlySummary,
  getByCategorySummary,
  getSubscriptionAlerts,
} from "./api";
import UploadForm from "./components/UploadForm";
import CategoryChart from "./components/CategoryChart";
import MonthlyBarChart from "./components/MonthlyBarChart";
import TransactionTable from "./components/TransactionTable";

function App() {
  const [transactions, setTransactions] = useState([]);
  const [monthly, setMonthly] = useState([]);
  const [byCategory, setByCategory] = useState([]);
  const [alerts, setAlerts] = useState([]);

  function refresh() {
    listTransactions().then((res) => setTransactions(res.data));
    getMonthlySummary().then((res) => setMonthly(res.data));
    getByCategorySummary().then((res) => setByCategory(res.data));
    getSubscriptionAlerts().then((res) => setAlerts(res.data));
  }

  useEffect(() => {
    refresh();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <h1 className="text-3xl font-bold text-slate-800 mb-6">
        Personal Finance Dashboard
      </h1>

      {alerts.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-300 text-yellow-800 p-4 rounded-lg mb-6">
          <p className="font-semibold mb-1">⚠️ Subscription increases detected</p>
          <ul className="text-sm list-disc list-inside">
            {alerts.map((a, i) => (
              <li key={i}>
                {a.description}: {a.previous_amount} → {a.current_amount} (+
                {a.increase})
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <UploadForm onUploaded={refresh} />
        <CategoryChart data={byCategory} />
      </div>

      <div className="mb-6">
        <MonthlyBarChart data={monthly} />
      </div>

      <div className="bg-white border border-slate-200 shadow-sm p-4 rounded-lg">
        <h2 className="text-lg font-semibold text-slate-800 mb-3">
          Transactions
        </h2>
        <TransactionTable transactions={transactions} onChanged={refresh} />
      </div>
    </div>
  );
}

export default App;