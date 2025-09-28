from typing import Annotated

from fastapi import (
    APIRouter,
    status,
)
from fastapi.params import Depends

from .crud import storage

from schemas.movie_url import (
    Movie,
)
from .dependencies import read_movie_slug

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


@router.delete(
    "/{movie_slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie Not Found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie 'slug' not found",
                    },
                },
            },
        },
    },
)
def delete_movie(
    slug: Annotated[
        Movie,
        Depends(read_movie_slug),
    ],
) -> None:
    storage.delete(movie=slug)
