from fastapi import APIRouter

router = APIRouter(prefix="/student/profile", tags=["Student Profile"])

@router.get("/{student_id}")
def get_student_profile(student_id: int):
    return {"student_id": student_id, "profile": "Profile details here"}