from fastapi import APIRouter

router = APIRouter()

@router.get("/admin")
def read_admin():
    return {"message": "Admin endpoint"}

