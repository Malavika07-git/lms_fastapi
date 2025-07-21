# routers/utility/resources.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.post("/", response_model=schemas.ResourceOut)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    faculty = db.query(models.Faculty).filter(models.Faculty.id == resource.uploaded_by).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    new_resource = models.Resource(**resource.dict())
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource

@router.get("/", response_model=List[schemas.ResourceOut])
def get_resources(db: Session = Depends(get_db)):
    return db.query(models.Resource).all()
