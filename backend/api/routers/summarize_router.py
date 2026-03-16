from fastapi import APIRouter

router = APIRouter()

@router.get("/summarize")
def read_summarize():
    return {"message": "Summarize endpoint"}