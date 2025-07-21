from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import SectionCourseFaculty
from database import get_db
import schemas

router = APIRouter(prefix="/admin/section-course-faculty", tags=["Admin - SectionCourseFaculty"])

@router.post("/", response_model=schemas.SectionCourseFacultyOut)
def create_mapping(data: schemas.SectionCourseFacultyCreate, db: Session = Depends(get_db)):
    mapping = SectionCourseFaculty(**data.dict())
    db.add(mapping)
    db.commit()
    db.refresh(mapping)
    return mapping

@router.get("/", response_model=List[schemas.SectionCourseFacultyOut])
def get_all_mappings(db: Session = Depends(get_db)):
    return db.query(SectionCourseFaculty).all()
