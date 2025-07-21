from fastapi import APIRouter

router = APIRouter(prefix="/admin/reports", tags=["Admin Reports"])

@router.get("/")
def generate_report():
    return {"message": "Admin report generated"}
