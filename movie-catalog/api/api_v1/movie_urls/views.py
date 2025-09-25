import random


from fastapi import (
    APIRouter,
    status,
)

from .crud import MOVIES

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
    return MOVIES


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_create: Movie):
    # noinspection PyArgumentList
    return Movie(
        **movie_create.model_dump(),
    )
