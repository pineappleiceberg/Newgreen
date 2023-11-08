from sqlalchemy.orm import Session
import hashlib
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashlib.sha512(user.password.encode()).hexdigest()
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(db: Session, email: str, password: str):
    input_hashed_password = hashlib.sha512(password.encode()).hexdigest()
    user = db.query(models.User).filter(models.User.email == email).first()

    if user:
        if user.hashed_password == input_hashed_password:
            return user
    return None

def get_budget_items(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.BudgetEntry).offset(skip).limit(limit).all()

def get_budget_items_for_user(db: Session, user_id: int):
    budget_items = db.query(models.BudgetEntry).filter(models.BudgetEntry.user_id == user_id).all()

    return budget_items

def create_user_budget_item(db: Session, budget_items: schemas.BudgetItem, user_id: int):
    db_budget_items = models.BudgetEntry(**budget_items.dict(), user_id=user_id)
    db.add(db_budget_items)
    db.commit()
    db.refresh(db_budget_items)

    return db_budget_items


