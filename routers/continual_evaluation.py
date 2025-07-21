from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import ContinualEvaluationCreate, ContinualEvaluationOut
from models import ContinualEvaluation, Student, Course

router = APIRouter(prefix="/continual-evaluation", tags=["Continual Evaluation"])

# Add new continual evaluation record
@router.post("/", response_model=ContinualEvaluationOut)
def create_evaluation(evaluation: ContinualEvaluationCreate, db: Session = Depends(get_db)):
    # Check if student and course exist
    student = db.query(Student).filter(Student.id == evaluation.student_id).first()
    course = db.query(Course).filter(Course.id == evaluation.course_id).first()
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")

    new_eval = ContinualEvaluation(
        student_id=evaluation.student_id,
        course_id=evaluation.course_id,
        assessment_name=evaluation.assessment_name,
        marks_obtained=evaluation.marks_obtained,
        total_marks=evaluation.total_marks
    )
    db.add(new_eval)
    db.commit()
    db.refresh(new_eval)
    return new_eval

# Get all evaluations
@router.get("/", response_model=list[ContinualEvaluationOut])
def get_all_evaluations(db: Session = Depends(get_db)):
    return db.query(ContinualEvaluation).all()

# Get evaluations for a specific student
@router.get("/student/{student_id}", response_model=list[ContinualEvaluationOut])
def get_student_evaluations(student_id: int, db: Session = Depends(get_db)):
    return db.query(ContinualEvaluation).filter(ContinualEvaluation.student_id == student_id).all()
