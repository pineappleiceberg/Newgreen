from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel


from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message":"Welcome to Newgreen"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post('/createuser/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    return crud.create_user(db=db, user=user)



@app.get('/getusers/', response_model=List[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)

    return users

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login/", response_model=schemas.User)
def login(request: Request, req_body: LoginRequest, db: Session = Depends(get_db)):
    db_user = crud.login_user(db, email=req_body.email, password=req_body.password)

    if db_user != None:
        return db_user
    else:
        raise HTTPException(status_code=400, detail="No account with those credentials could be authenticataed")


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_user


@app.post('/users/{user_id}/budgetitems/', response_model=schemas.BudgetItem)
def create_budget_item(user_id: int, budget_item: schemas.BudgetCreate, db: Session = Depends(get_db)):
    return crud.create_user_budget_item(db=db, budget_items=budget_item, user_id=user_id)


@app.get('/budgetitems/', response_model=List[schemas.BudgetItem])
def read_budget_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    budget_items = crud.get_budget_items(db, skip=skip, limit=limit)

    return budget_items


@app.get('/users/{user_id}/getbudgetitems/', response_model=List[schemas.BudgetItem], tags=["BudgetItems"])
def get_budget_items_for_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    budget_items = crud.get_budget_items_for_user(db, user_id=user_id)

    return budget_items