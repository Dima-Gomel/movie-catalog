import random


from fastapi import (
    APIRouter,
    status,
    Form,
)

from .crud import MOVIES

from schemas.movie_url import Movie

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
def create_movie(
    title: Annotated[str, Form()],
    year: Annotated[int, Form()],
    description: Annotated[str, Form()],
    genre: Annotated[str, Form()],
):
    return Movie(
        movie_id=random.randint(4, 20),
        title=title,
        year=year,
        description=description,
        genre=genre,
    )
