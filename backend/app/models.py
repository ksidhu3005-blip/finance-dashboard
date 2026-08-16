from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from datetime import datetime
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, default="Uncategorized")
    source_file = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CategoryRule(Base):
    __tablename__ = "category_rules"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)