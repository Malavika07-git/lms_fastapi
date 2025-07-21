from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Float,Enum, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


Base = declarative_base()

# ---------------------- User ----------------------
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)

    student = relationship("Student", back_populates="user", uselist=False)
    faculty = relationship("Faculty", back_populates="user", uselist=False)


# ---------------------- Department ----------------------
class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    students = relationship("Student", back_populates="department")
    faculties = relationship("Faculty", back_populates="department")


# ---------------------- Faculty ----------------------
class Faculty(Base):
    __tablename__ = 'faculties'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    department_id = Column(Integer, ForeignKey('departments.id'))

    user = relationship("User", back_populates="faculty")
    department = relationship("Department", back_populates="faculties")
    courses = relationship("Course", back_populates="faculty")
    classes = relationship("Class", back_populates="faculty")
    resources = relationship("Resource", back_populates="uploader")
    announcements = relationship("Announcement", back_populates="faculty")
    continual_evaluations = relationship("ContinualEvaluation", back_populates="faculty")
    grades = relationship("Grade", back_populates="faculty")  



# ---------------------- Student ----------------------
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    enrollment_number = Column(String, unique=True)
    dob = Column(Date)
    gender = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    department_id = Column(Integer, ForeignKey('departments.id'))

    user = relationship("User", back_populates="student")
    department = relationship("Department", back_populates="students")
    attendances = relationship("Attendance", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    student_classes = relationship("StudentClass", back_populates="student")
    continual_evaluations = relationship("ContinualEvaluation", back_populates="student")


# ---------------------- Courses ----------------------
class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    units = Column(Integer)

    faculty_id = Column(Integer, ForeignKey('faculties.id'))

    faculty = relationship("Faculty", back_populates="courses")
    attendances = relationship("Attendance", back_populates="course")
    grades = relationship("Grade", back_populates="course")
    classes = relationship("Class", back_populates="course")
    section_course_links = relationship("SectionCourseFaculty", back_populates="course")
    continual_evaluations = relationship("ContinualEvaluation", back_populates="course")


# ---------------------- Classes ----------------------
class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    section = Column(String, nullable=False)

    faculty_id = Column(Integer, ForeignKey('faculties.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

    faculty = relationship("Faculty", back_populates="classes")
    course = relationship("Course", back_populates="classes")
    student_classes = relationship("StudentClass", back_populates="class_")
    section_course_links = relationship("SectionCourseFaculty", back_populates="class_")


# ---------------------- StudentClass (Link Table) ----------------------
class StudentClass(Base):
    __tablename__ = 'student_classes'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    class_id = Column(Integer, ForeignKey('classes.id'))

    student = relationship("Student", back_populates="student_classes")
    class_ = relationship("Class", back_populates="student_classes")


# ---------------------- Attendance ----------------------
class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    date = Column(Date)
    attended = Column(Boolean)

    student = relationship("Student", back_populates="attendances")
    course = relationship("Course", back_populates="attendances")


# ---------------------- Grades ----------------------
class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    faculty_id = Column(Integer, ForeignKey('faculties.id'))
    semester = Column(String)
    grade = Column(String)
    units = Column(Integer)
    cgpa = Column(Float)

    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")
    faculty = relationship("Faculty", back_populates="grades")


# ---------------------- Section-Course-Faculty Link ----------------------
class SectionCourseFaculty(Base):
    __tablename__ = "section_course_faculty"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)

    course = relationship("Course", back_populates="section_course_links")
    faculty = relationship("Faculty", back_populates="section_course_links")
    class_ = relationship("Class", back_populates="section_course_links")


# ---------------------- Resources ----------------------
class ResourceType(str, enum.Enum):
    link = "link"
    material = "material"

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(Enum(ResourceType), nullable=False)
    content_url = Column(Text, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    uploader = relationship("Faculty", back_populates="resources")


# ---------------------- Continual Evaluations ----------------------
class ContinualEvaluation(Base):
    __tablename__ = "continual_evaluations"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculties.id'), nullable=True)

    component = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    date = Column(Date, nullable=True)

    student = relationship("Student", back_populates="continual_evaluations")
    course = relationship("Course", back_populates="continual_evaluations")
    faculty = relationship("Faculty", back_populates="continual_evaluations")


# ---------------------- Announcements ----------------------
class Announcement(Base):
    __tablename__ = "announcements"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    posted_by = Column(Integer, ForeignKey("faculties.id"))

    faculty = relationship("Faculty", back_populates="announcements")


# ---------------------- MyInfo (Optional Info) ----------------------
class MyInfo(Base):
    __tablename__ = "my_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    blood_group = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    religion = Column(String, nullable=True)



