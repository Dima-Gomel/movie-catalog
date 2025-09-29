from fastapi import (
    status,
    APIRouter,
)

from api.api_v1.movie_urls.crud import storage
from api.api_v1.movie_urls.views.details_views import router as detail_router

from schemas.movie_url import (
    Movie,
)

router = APIRouter(
    prefix="/movies",
)

router.include_router(detail_router)


@router.get(
    "/",
    response_model=list[Movie],
)
def read_movie_details():
    return storage.get()


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_create: Movie):
    return storage.create(movie_create)
