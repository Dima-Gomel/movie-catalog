from fastapi import APIRouter
from .movie_urls.views import router as movie_urls_router

router = APIRouter(
    prefix="/v1",
    tags=["Movies"],
)

router.include_router(movie_urls_router)
