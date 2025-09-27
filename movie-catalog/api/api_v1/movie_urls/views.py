from fastapi import (
    APIRouter,
    status,
)

from .crud import storage

from schemas.movie_url import (
    Movie,
)

router = APIRouter(
    prefix="/movies",
)


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
