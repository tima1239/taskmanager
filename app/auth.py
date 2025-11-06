from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=3)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        return user
    except (JWTError, IndexError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
