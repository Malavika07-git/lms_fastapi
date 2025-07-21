from fastapi import APIRouter

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])

@router.get("/")
def get_dashboard_data():
    return {"message": "Admin dashboard data"}
