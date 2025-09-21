from fastapi import APIRouter
from .api_v1 import router as api_router

router = APIRouter(
    prefix="/api",
)

router.include_router(api_router)
