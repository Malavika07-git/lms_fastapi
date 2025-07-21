from fastapi import APIRouter

router = APIRouter(prefix="/student/progress", tags=["Student Progress"])

@router.get("/{student_id}")
def get_progress(student_id: int):
    return {"student_id": student_id, "progress": "Progress tracking here you can check"}