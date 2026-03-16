from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def read_auth():
    return {"message": "Authentication endpoint"}