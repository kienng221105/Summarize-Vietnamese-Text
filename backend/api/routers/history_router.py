from fastapi import APIRouter

router = APIRouter()

@router.get("/history")
def read_history():
    return {"message": "History endpoint"}