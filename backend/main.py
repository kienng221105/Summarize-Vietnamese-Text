from fastapi import FastAPI
from backend.api.routers import history_router, auth_router, summarize_router, admin_router

app = FastAPI(
    title="Vietnamese Text Summaryizer API",
    description="An API for summarizing Vietnamese text using a pre-trained model.",
    version="1.0.0",
)

app.include_router(history_router.router, prefix="/history", tags=["History"])
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
app.include_router(summarize_router.router, prefix="/summarize", tags=["Summarization"])
app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Vietnamese Text Summaryizer API!"}
