from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app import models, crud
from app.routers import transactions

app = FastAPI(title="Finance Dashboard API")

# Create tables if they don't exist yet (safe to run every startup)
Base.metadata.create_all(bind=engine)

# Seed starter category rules once, so the app isn't empty on first run
db = SessionLocal()
crud.seed_default_rules(db)
db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://finance-dashboard-tau-lyart.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router)


@app.get("/health")
def health():
    return {"status": "ok"}