from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class BudgetEntry(Base):
    __tablename__ = 'budget'
    title = Column(String)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    note = Column(String)
    amount = Column(Float)
    pastBudget = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(ForeignKey("user.id"))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    authtoken = Column(String)
    hashed_password = Column(String)
    email = Column(String)