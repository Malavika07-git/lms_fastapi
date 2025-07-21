from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal
import models, schemas

router = APIRouter(prefix="/students", tags=["Students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/", response_model=List[schemas.StudentOut])
def get_students(
    class_id: Optional[int] = Query(None),
    department_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(models.Student)

    if class_id is not None:
        query = query.filter(models.Student.class_id == class_id)

    if department_id is not None:
        query = query.filter(models.Student.department_id == department_id)

    return query.offset(skip).limit(limit).all()
