from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class TransactionOut(BaseModel):
    id: int
    date: date
    description: str
    amount: float
    category: str
    source_file: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionUpdate(BaseModel):
    category: str


class CategoryRuleCreate(BaseModel):
    keyword: str
    category: str


class CategoryRuleOut(BaseModel):
    id: int
    keyword: str
    category: str

    class Config:
        from_attributes = True


class UploadResult(BaseModel):
    rows_imported: int
    rows_skipped_duplicates: int
    message: str