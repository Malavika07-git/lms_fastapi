from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Constants
SECRET_KEY = "your-secret-key"  # 🔒 Replace with a secure key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login", response_model=schemas.TokenResponse)
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    role = data.role.lower()
    user = None

    if role == "student":
        student = db.query(models.Student).filter(models.Student.id == int(data.identifier)).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        user = db.query(models.User).filter(models.User.id == student.user_id).first()

    elif role == "faculty":
        faculty = db.query(models.Faculty).filter(models.Faculty.id == int(data.identifier)).first()
        if not faculty:
            raise HTTPException(status_code=404, detail="Faculty not found")
        user = db.query(models.User).filter(models.User.id == faculty.user_id).first()

    elif role == "admin":
        user = db.query(models.User).filter(models.User.email == data.identifier, models.User.role == "admin").first()
        if not user:
            raise HTTPException(status_code=404, detail="Admin not found")

    else:
        raise HTTPException(status_code=400, detail="Invalid role")

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}
