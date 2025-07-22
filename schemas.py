from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from pydantic import  EmailStr

# ----------------- Authentication -----------------

class MyInfoCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    nationality: Optional[str] = None

class MyInfoOut(MyInfoCreate):
    id: int

    class Config:
        from_attributes = True 

class UserLogin(BaseModel):
    identifier: str  # Can be student ID, faculty ID, or email (for admin)
    password: str
    role: str  # "student", "faculty", "admin"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ----------------- User -----------------

class UserBase(BaseModel):
    username: str
    email: str
    role: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str  # "student", "faculty", or "admin"

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# ----------------- Student -----------------

class StudentBase(BaseModel):
    name: str
    enrollment_number: str
    dob: date
    gender: str
    department_id: int

class StudentCreate(StudentBase):
    user_id: int
    department_id: int
    class_id: int

class StudentOut(StudentBase):
    id: int
    user_id: int
    department_id: int
    class_id: int


    class Config:
        orm_mode = True

class StudentRegister(BaseModel):
    name: str
    email: str
    class_id: int  # Section the student selects

class StudentClassCreate(BaseModel):
    student_id: int
    class_id: int

class StudentClassOut(StudentClassCreate):
    id: int

    class Config:
        orm_mode = True

# ----------------- Faculty -----------------

class FacultyCreate(BaseModel):
    name: str
    user_id: int

class FacultyOut(BaseModel):
    id: int
    name: str
    user: UserOut

    class Config:
        orm_mode = True

# ----------------- Course -----------------

class CourseCreate(BaseModel):
    code: str
    name: str
    units: int
    faculty_id: int

class CourseOut(CourseCreate):
    id: int

    class Config:
        orm_mode = True

# ----------------- Class (Section-Course-Faculty) -----------------

class ClassCreate(BaseModel):
    section: str
    faculty_id: int
    course_id: int

class ClassOut(ClassCreate):
    id: int

    class Config:
        orm_mode = True

class SectionCourseFacultyBase(BaseModel):
    class_id: int
    course_id: int
    faculty_id: int

class SectionCourseFacultyCreate(SectionCourseFacultyBase):
    pass

class SectionCourseFacultyOut(SectionCourseFacultyBase):
    id: int

    class Config:
        orm_mode = True

# ----------------- Department -----------------

class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int

    class Config:
        orm_mode = True

# ----------------- Attendance -----------------

class AttendanceCreate(BaseModel):
    student_id: int
    course_id: int
    date: date
    attended: bool

class AttendanceOut(AttendanceCreate):
    id: int

    class Config:
        orm_mode = True

# ----------------- Grades -----------------

class GradeCreate(BaseModel):
    student_id: int
    course_id: int
    faculty_id: int
    semester: str
    grade: str
    units: int
    cgpa: float

class GradeOut(GradeCreate):
    id: int

    class Config:
        orm_mode = True

class ResourceType(str, Enum):
    link = "link"
    material = "material"

class ResourceBase(BaseModel):
    title: str
    type: ResourceType
    content_url: str

class ResourceCreate(ResourceBase):
    uploaded_by: int

class ResourceOut(ResourceBase):
    id: int
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

class  ContinualEvaluationBase(BaseModel):
    student_id: int
    course_id: int
    faculty_id: Optional[int] = None
    component: str
    score: float
    total: float
    date: Optional[date] = None

# For creation
class ContinualEvaluationCreate(ContinualEvaluationBase):
    pass

# For reading
class ContinualEvaluationOut(ContinualEvaluationBase):
    id: int

    class Config:
        orm_mode = True        

class AnnouncementBase(BaseModel):
    title: str
    content: str
    created_by: int  # Faculty ID
    class_id: Optional[int] = None


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementOut(AnnouncementBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  


class FacultyCreate(BaseModel):
    user_id: int
    department_id: int

class FacultyOut(BaseModel):
    id: int
    user_id: int
    department_id: int

class FacultyUpdate(BaseModel):
    department_id: Optional[int] = None    

    class Config:
        orm_mode = True  # Needed in Pydantic v2
 
class FacultyDepartmentOut(FacultyOut):
    department: Optional[DepartmentOut]