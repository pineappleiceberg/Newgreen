from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class BudgetEntry(Base):
    __tablename__ = 'budget'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    note = Column(String)
    amount = Column(Float)
    pastBudget = Column(Boolean)
    user_id = Column(ForeignKey())

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    authtoken = Column(String)