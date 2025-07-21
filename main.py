from fastapi import FastAPI
from database import Base, engine
from routers import  students, courses, grades, attendance, myinfo,resources, continual_evaluation, annoncemant
from routers import faculty_router
from routers import auth as auth_router  
from routers.utility import auth as auth_utils
from routers.admin import dashboard, reports, studentfaculitycourse
from routers.student import profile, progress
from routers.admin import dashboard, reports, studentfaculitycourse
from routers.student import profile, progress


# Create tables
from models import *
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LMS Backend")

# Include routers
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(grades.router)
app.include_router(attendance.router)
app.include_router(faculty_router.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
app.include_router(profile.router)
app.include_router(progress.router)
app.include_router(studentfaculitycourse.router)
app.include_router(auth_router.router)  # ✅ Correct router
app.include_router(myinfo.router)
app.include_router(resources.router)
app.include_router(continual_evaluation.router)
app.include_router(annoncemant.router)


@app.get("/")
def root():
    return {"message": "Welcome everone to my LMS website"}

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# Serve static files (HTML/CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/signup", response_class=HTMLResponse)
def serve_signup():
    with open(os.path.join("static", "signup.html"), "r") as f:
        return f.read()

