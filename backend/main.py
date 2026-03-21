from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.api.routers import history_router, auth_router, ai_router, admin_router, rating_router
import traceback
from backend.database.models import Base

app = FastAPI(
    title="Vietnamese Text Summaryizer API",
    description="An API for summarizing Vietnamese text using a pre-trained model.",
    version="1.0.0",
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("FATAL ERROR CAUGHT BY GLOBAL HANDLER:")
    traceback.print_exc()
    import backend.database.models as models
    print(f"MODELS DIR: {dir(models)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"INTERNAL ERROR: {str(exc)}", 
            "models_dir": dir(models),
            "traceback": traceback.format_exc()
        },
    )

app.include_router(history_router.router, prefix="/history", tags=["History"])
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
app.include_router(ai_router.router, prefix="/ai", tags=["Summarization"])
app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])
app.include_router(rating_router.router, prefix="/rating", tags=["Rating"])

@app.get("/")
def read_root():
    """
    Endpoint mặc định kiểm tra trạng thái API.
    - Input: Không có.
    - Output: Thông điệp chào mừng.
    """
    return {"message": "Welcome to the Vietnamese Text Summaryizer API!"}
