from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/myinfo", tags=["My Info"])

@router.post("/", response_model=schemas.MyInfoOut)
def create_my_info(data: schemas.MyInfoCreate, db: Session = Depends(get_db)):
    existing = db.query(models.MyInfo).filter(models.MyInfo.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    new_info = models.MyInfo(**data.dict())
    db.add(new_info)
    db.commit()
    db.refresh(new_info)
    return new_info

@router.get("/", response_model=list[schemas.MyInfoOut])
def get_all_my_info(db: Session = Depends(get_db)):
    return db.query(models.MyInfo).all()
