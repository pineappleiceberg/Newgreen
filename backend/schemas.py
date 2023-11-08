from typing import List, Optional
from pydantic import BaseModel


class BudgetBase(BaseModel):
    title: str
    amount: float
    note: Optional[str] = "-"

class BudgetCreate(BudgetBase):
    pass


class BudgetItem(BudgetBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str



class User(UserBase):
    id: int
    budget_items: List[BudgetItem] = []

    class Config:
        orm_mode = True