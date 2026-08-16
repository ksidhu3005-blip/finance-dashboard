import { useState } from "react";
import { recategorizeTransaction } from "../api";

const CATEGORIES = [
  "Housing",
  "Transport",
  "Shopping",
  "Subscriptions",
  "Groceries",
  "Income",
  "Utilities",
  "Dining",
  "Uncategorized",
];

function TransactionTable({ transactions, onChanged }) {
  const [editingId, setEditingId] = useState(null);

  async function handleRecategorize(id, category) {
    await recategorizeTransaction(id, category);
    setEditingId(null);
    onChanged();
  }

  if (transactions.length === 0) {
    return (
      <p className="text-slate-500 italic">
        No transactions yet — upload a CSV to get started.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-slate-800 text-sm">
        <thead>
          <tr className="border-b border-slate-200 text-slate-500">
            <th className="py-2">Date</th>
            <th>Description</th>
            <th>Amount</th>
            <th>Category</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((t) => (
            <tr key={t.id} className="border-b border-slate-100">
              <td className="py-2">{t.date}</td>
              <td>{t.description}</td>
              <td className={t.amount < 0 ? "text-red-600" : "text-green-600"}>
                {t.amount.toFixed(2)}
              </td>
              <td>
                {editingId === t.id ? (
                  <select
                    autoFocus
                    defaultValue={t.category}
                    onChange={(e) => handleRecategorize(t.id, e.target.value)}
                    onBlur={() => setEditingId(null)}
                    className="bg-slate-100 text-slate-800 p-1 rounded text-xs border border-slate-300"
                  >
                    {CATEGORIES.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                ) : (
                  <button
                    onClick={() => setEditingId(t.id)}
                    className="text-xs px-2 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700"
                  >
                    {t.category}
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionTable;