from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserLogin, TokenResponse
from database import get_db
from auth import verify_password, create_access_token

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/", response_model=TokenResponse)
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.identifier).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if user.role != data.role.lower():
        raise HTTPException(status_code=403, detail=f"You are not {data.role}")

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
