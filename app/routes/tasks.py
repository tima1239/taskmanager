from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/")
def get_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role == "admin":
        return db.query(Task).all()
    return db.query(Task).filter(Task.owner_id == user.id).all()

@router.post("/")
def create_task(title: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = Task(title=title, owner_id=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if user.role != "admin" and task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Нет доступа")
    db.delete(task)
    db.commit()
    return {"message": "Задача удалена"}
