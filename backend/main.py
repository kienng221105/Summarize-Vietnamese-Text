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
    print(f"Lỗi hệ thống (500) tại {request.url.path}: {str(exc)}")
    traceback.print_exc()
    # Không trả về traceback hoặc dữ liệu nội bộ cho client để bảo mật
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error. Please try again later."
        },
    )

app.include_router(history_router.router, prefix="/history", tags=["History"])
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
app.include_router(ai_router.router, prefix="/ai", tags=["Summarization"])
app.include_router(admin_router.router, prefix="/admin", tags=["Admin"])
app.include_router(rating_router.router, prefix="/rating", tags=["Rating"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Vietnamese Text Summaryizer API!"}
