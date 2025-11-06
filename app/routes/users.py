from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    return {"message": "Регистрация успешна!"}

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
