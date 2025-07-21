from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/faculty",
    tags=["Faculty"]
)

@router.post("/add-grade", response_model=schemas.GradeOut)
def add_grade(grade_data: schemas.GradeCreate, db: Session = Depends(get_db)):
    # Optional: Validate student and course existence
    student = db.query(models.Student).filter(models.Student.id == grade_data.student_id).first()
    course = db.query(models.Course).filter(models.Course.id == grade_data.course_id).first()

    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")

    new_grade = models.Grade(
        student_id=grade_data.student_id,
        course_id=grade_data.course_id,
        semester=grade_data.semester,
        grade=grade_data.grade,
        units=grade_data.units,
        cgpa=grade_data.cgpa
    )

    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)
    return new_grade

@router.get("/grades/filter", response_model=list[schemas.GradeOut])
def filter_grades(
    student_id: int = None,
    course_id: int = None,
    semester: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Grade)
    if student_id:
        query = query.filter(models.Grade.student_id == student_id)
    if course_id:
        query = query.filter(models.Grade.course_id == course_id)
    if semester:
        query = query.filter(models.Grade.semester == semester)
    
    return query.all()

