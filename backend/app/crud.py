import pandas as pd
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models import Transaction, CategoryRule
from app.categorize import categorize, DEFAULT_RULES


# ---------- Category rules ----------

def seed_default_rules(db: Session):
    """Run once at startup — insert starter rules if the table is empty."""
    existing = db.query(CategoryRule).count()
    if existing == 0:
        for rule in DEFAULT_RULES:
            db.add(CategoryRule(keyword=rule["keyword"], category=rule["category"]))
        db.commit()


def get_rules_as_dicts(db: Session) -> list[dict]:
    rules = db.query(CategoryRule).all()
    return [{"keyword": r.keyword, "category": r.category} for r in rules]


def create_rule(db: Session, keyword: str, category: str):
    obj = CategoryRule(keyword=keyword.lower(), category=category)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_rules(db: Session):
    return db.query(CategoryRule).all()


# ---------- CSV import pipeline ----------

def parse_csv(file_bytes: bytes) -> pd.DataFrame:
    """
    Load a CSV upload into a normalized DataFrame.
    Handles a couple of common column-naming variants so it isn't fragile
    to one specific bank's export format.
    """
    from io import BytesIO

    df = pd.read_csv(BytesIO(file_bytes))

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    rename_map = {
        "transaction_date": "date",
        "posting_date": "date",
        "narrative": "description",
        "memo": "description",
        "value": "amount",
        "debit": "amount",
    }
    df = df.rename(columns=rename_map)

    required = {"date", "description", "amount"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    df = df.dropna(how="all")
    df["description"] = df["description"].astype(str).str.strip()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

    df = df.dropna(subset=["date", "amount", "description"])
    df = df[df["description"] != ""]

    return df


def import_transactions(db: Session, df: pd.DataFrame, source_file: str):
    rules = get_rules_as_dicts(db)

    imported = 0
    skipped = 0

    for _, row in df.iterrows():
        exists = (
            db.query(Transaction)
            .filter(
                Transaction.date == row["date"],
                Transaction.description == row["description"],
                Transaction.amount == row["amount"],
            )
            .first()
        )
        if exists:
            skipped += 1
            continue

        category = categorize(row["description"], rules)
        txn = Transaction(
            date=row["date"],
            description=row["description"],
            amount=float(row["amount"]),
            category=category,
            source_file=source_file,
        )
        db.add(txn)
        imported += 1

    db.commit()
    return imported, skipped


# ---------- Transactions ----------

def get_transactions(db: Session, category: str | None = None, limit: int = 500):
    query = db.query(Transaction).order_by(Transaction.date.desc())
    if category:
        query = query.filter(Transaction.category == category)
    return query.limit(limit).all()


def update_transaction_category(db: Session, transaction_id: int, new_category: str):
    txn = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not txn:
        return None

    keyword = txn.description.lower().split()[0] if txn.description else None
    if keyword:
        existing_rule = db.query(CategoryRule).filter(CategoryRule.keyword == keyword).first()
        if not existing_rule:
            db.add(CategoryRule(keyword=keyword, category=new_category))

    txn.category = new_category
    db.commit()
    db.refresh(txn)
    return txn


# ---------- Summaries ----------

def get_monthly_summary(db: Session):
    results = (
        db.query(
            extract("year", Transaction.date).label("year"),
            extract("month", Transaction.date).label("month"),
            func.sum(Transaction.amount).label("total"),
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )
    return [
        {"month": f"{int(r.year)}-{int(r.month):02d}", "total": round(r.total, 2)}
        for r in results
    ]


def get_by_category_summary(db: Session, month: str | None = None):
    query = db.query(
        Transaction.category, func.sum(Transaction.amount).label("total")
    )
    if month:
        year, mon = month.split("-")
        query = query.filter(
            extract("year", Transaction.date) == int(year),
            extract("month", Transaction.date) == int(mon),
        )
    results = query.group_by(Transaction.category).all()
    return [{"category": r.category, "total": round(r.total, 2)} for r in results]


def get_subscription_increases(db: Session):
    """
    Compare this month's recurring charges against last month's for the
    same description, flag any that increased.
    """
    today = date.today()
    this_month_start = today.replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    this_month_txns = (
        db.query(Transaction)
        .filter(Transaction.date >= this_month_start, Transaction.date <= today)
        .all()
    )
    last_month_txns = (
        db.query(Transaction)
        .filter(
            Transaction.date >= last_month_start, Transaction.date <= last_month_end
        )
        .all()
    )

    last_month_map = {t.description: t.amount for t in last_month_txns}

    increases = []
    for t in this_month_txns:
        prior = last_month_map.get(t.description)
        if prior is not None and t.amount > prior:
            increases.append(
                {
                    "description": t.description,
                    "previous_amount": prior,
                    "current_amount": t.amount,
                    "increase": round(t.amount - prior, 2),
                }
            )
    return increases