from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Grade, User
from schemas import GradeCreate, GradeOut
from routers.utility.auth import get_current_user, faculty_required 

router = APIRouter(prefix="/grades", tags=["Grades"])

@router.post("/", response_model=GradeOut)
def add_grade(grade: GradeCreate, db: Session = Depends(get_db),current_user: User = Depends(faculty_required) ):
    db_grade = Grade(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.get("/student/{student_id}", response_model=list[GradeOut])
def get_grades_by_student(student_id: int, db: Session = Depends(get_db)):
    grades = db.query(Grade).filter(Grade.student_id == student_id).all()
    return grades
