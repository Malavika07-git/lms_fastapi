from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import SectionCourseFaculty
from database import get_db
import schemas

router = APIRouter(prefix="/admin/section-course-faculty", tags=["Admin - SectionCourseFaculty"])

@router.post("/", response_model=schemas.FacultyOut)
def create_faculty(faculty: schemas.FacultyCreate, db: Session = Depends(get_db)):
    new_faculty = Faculty(**faculty.dict())
    db.add(new_faculty)
    db.commit()
    db.refresh(new_faculty)
    return new_faculty

@router.get("/", response_model=list[schemas.FacultyOut])
def get_all_faculty(db: Session = Depends(get_db)):
    return db.query(Faculty).all()

@router.get("/{faculty_id}", response_model=schemas.FacultyOut)
def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    faculty = db.query(Faculty).get(faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty

@router.put("/{faculty_id}", response_model=schemas.FacultyOut)
def update_faculty(faculty_id: int, update_data: schemas.FacultyUpdate, db: Session = Depends(get_db)):
    faculty = db.query(Faculty).get(faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(faculty, field, value)
    db.commit()
    db.refresh(faculty)
    return faculty

@router.delete("/{faculty_id}")
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    faculty = db.query(Faculty).get(faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    db.delete(faculty)
    db.commit()
    return {"detail": "Faculty deleted successfully"}

@router.get("/{faculty_id}/assignments", response_model=List[schemas.SectionCourseFacultyOut])
def get_faculty_assignments(faculty_id: int, db: Session = Depends(get_db)):
    return db.query(SectionCourseFaculty).filter_by(faculty_id=faculty_id).all()
