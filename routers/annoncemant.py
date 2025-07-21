from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Announcement, Faculty
from schemas import AnnouncementCreate, AnnouncementOut

router = APIRouter(
    prefix="/announcements",
    tags=["Announcements"]
)

# Create an announcement
@router.post("/", response_model=AnnouncementOut)
def create_announcement(announcement: AnnouncementCreate, db: Session = Depends(get_db)):
    faculty = db.query(Faculty).filter(Faculty.id == announcement.faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    new_announcement = Announcement(
        title=announcement.title,
        message=announcement.message,
        faculty_id=announcement.faculty_id
    )
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return new_announcement

# Get all announcements
@router.get("/", response_model=list[AnnouncementOut])
def get_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).order_by(Announcement.created_at.desc()).all()

# Get a single announcement
@router.get("/{announcement_id}", response_model=AnnouncementOut)
def get_announcement(announcement_id: int, db: Session = Depends(get_db)):
    ann = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return ann

# Delete an announcement
@router.delete("/{announcement_id}")
def delete_announcement(announcement_id: int, db: Session = Depends(get_db)):
    ann = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found")
    db.delete(ann)
    db.commit()
    return {"message": "Announcement deleted"}
