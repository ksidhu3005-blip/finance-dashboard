# Personal Finance Dashboard

Import a bank statement CSV, watch it get auto-categorized, and see exactly where your money goes each month — built to replace manually sorting through transactions by hand.

**Live app:** https://finance-dashboard-tau-lyart.vercel.app
**API:** https://finance-dashboard-s96v.onrender.com/health

---

## The Problem It Solves

Bank statements dump raw transactions with zero structure — every purchase looks the same whether it's rent or a coffee. This tool ingests a CSV export, automatically tags each transaction with a spending category using keyword rules, and visualizes the result so patterns (and unwanted subscription price hikes) become obvious at a glance instead of buried in a spreadsheet.

## Screenshots

**Dashboard overview — upload, alerts, and category breakdown**
![Dashboard overview](dashboard-1.png)

**Monthly totals and transaction list**
![Monthly totals](dashboard-2.png)

**Transaction table with auto-assigned categories**
![Transaction table](dashboard-3.png)

## Tech Stack

**Backend**
- FastAPI (Python)
- pandas (CSV parsing)
- PostgreSQL
- SQLAlchemy (ORM)

**Frontend**
- React (Vite)
- Tailwind CSS
- Chart.js

**Deployment**
- Backend + database: Render
- Frontend: Vercel

## Features

- **CSV upload** — parses messy bank export formats (handles common column-naming variants)
- **Auto-categorization** — 16 seeded keyword rules (rent → Housing, netflix → Subscriptions, etc.), falls back to "Uncategorized"
- **Idempotent imports** — re-uploading the same statement never creates duplicate rows (checked by date + description + amount)
- **Inline recategorization** — click any category badge to correct it; the system learns a new rule from the correction automatically
- **Spend-by-category chart** — doughnut chart showing proportion of spend per category
- **Monthly totals chart** — bar chart showing spend trend over time
- **Subscription increase alerts** — automatically flags any recurring charge that went up from the previous month

## Architecture

```
React Frontend (Vercel)
        |
        | HTTPS / JSON
        v
FastAPI Backend (Render)
        |
        | pandas (CSV parsing) + SQLAlchemy
        v
PostgreSQL Database (Render)
```

The backend keeps the categorization logic (`categorize.py`) as a standalone, dependency-free function — it takes a description and a list of rules, and returns a category. This makes it trivially testable in isolation and separate from the database/HTTP layers around it.

## Run It Locally

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:
```
DATABASE_URL=postgresql://user:password@localhost/finance_dashboard
```

Then run:
```bash
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`, interactive docs at `http://localhost:8000/docs`. Tables and 16 starter category rules are created automatically on first startup.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`.

### Testing the import pipeline

A synthetic 3-month sample bank statement (`sample_bank_statement.csv`) is included — upload it through the UI to see categorization, both charts, and the subscription-increase alert all populate immediately.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /transactions/upload | Upload and import a CSV bank statement |
| GET | /transactions | List transactions (optional category filter) |
| PATCH | /transactions/{id} | Recategorize a transaction |
| GET | /category-rules | List all keyword to category rules |
| POST | /category-rules | Add a new rule |
| GET | /summary/monthly | Total spend per month |
| GET | /summary/by-category | Spend grouped by category |
| GET | /alerts/subscription-increases | Recurring charges that increased vs. last month |
| GET | /health | Health check |

## What's Next

- Support for more bank CSV export formats
- A standalone scheduled script (`scripts/check_subscriptions.py`) to run the subscription-alert check independently via cron
- Automated tests with pytest
- CI pipeline via GitHub Actions

## Author

**Sandeep Kaur**
[GitHub](https://github.com/ksidhu3005-blip) - [LinkedIn](https://linkedin.com/in/sandeep-kaur-172272422)
