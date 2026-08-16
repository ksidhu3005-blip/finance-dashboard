from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(tags=["transactions"])


@router.post("/transactions/upload", response_model=schemas.UploadResult)
async def upload_transactions(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file")

    contents = await file.read()
    try:
        df = crud.parse_csv(contents)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    imported, skipped = crud.import_transactions(db, df, source_file=file.filename)

    return schemas.UploadResult(
        rows_imported=imported,
        rows_skipped_duplicates=skipped,
        message=f"Imported {imported} new transactions, skipped {skipped} duplicates.",
    )


@router.get("/transactions", response_model=List[schemas.TransactionOut])
def list_transactions(
    category: Optional[str] = None, db: Session = Depends(get_db)
):
    return crud.get_transactions(db, category=category)


@router.patch("/transactions/{transaction_id}", response_model=schemas.TransactionOut)
def recategorize_transaction(
    transaction_id: int, data: schemas.TransactionUpdate, db: Session = Depends(get_db)
):
    txn = crud.update_transaction_category(db, transaction_id, data.category)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return txn


@router.get("/category-rules", response_model=List[schemas.CategoryRuleOut])
def list_rules(db: Session = Depends(get_db)):
    return crud.get_rules(db)


@router.post("/category-rules", response_model=schemas.CategoryRuleOut, status_code=201)
def create_rule(data: schemas.CategoryRuleCreate, db: Session = Depends(get_db)):
    return crud.create_rule(db, data.keyword, data.category)


@router.get("/summary/monthly")
def summary_monthly(db: Session = Depends(get_db)):
    return crud.get_monthly_summary(db)


@router.get("/summary/by-category")
def summary_by_category(month: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_by_category_summary(db, month=month)


@router.get("/alerts/subscription-increases")
def subscription_increases(db: Session = Depends(get_db)):
    return crud.get_subscription_increases(db)