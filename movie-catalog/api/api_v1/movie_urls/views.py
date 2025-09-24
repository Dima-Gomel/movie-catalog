import random


from fastapi import (
    APIRouter,
    status,
    Form,
)

from .crud import MOVIES

from schemas.movie_url import (
    Movie,
    MovieCreate,
)

from typing import Annotated

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
def create_movie(movie_create: MovieCreate):

    return Movie(
        movie_id=random.randint(1, 20),
        **movie_create.model_dump(),
    )
