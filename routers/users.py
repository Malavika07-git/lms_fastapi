"""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
from models import User
from schemas import UserCreate, UserOut
from auth import get_password_hash  

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create the user
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        username=user.username,
        password=hashed_password,
        role=user.role.lower()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user"""

