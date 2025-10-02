from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi.params import Depends
from starlette import status

from api.api_v1.movie_urls.crud import storage
from api.api_v1.movie_urls.dependencies import prefetch_movie
from schemas.movie_url import (
    Movie,
    MovieUpdate,
    MoviePartialUpdate,
    MovieRead,
)

router = APIRouter(
    prefix="/{slug}",
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


MovieBySlug = Annotated[
    Movie,
    Depends(prefetch_movie),
]


@router.get(
    "/",
    response_model=MovieRead,
)
def read_movie_slug(movie: MovieBySlug) -> Movie:
    return movie


@router.put(
    "/",
    response_model=MovieRead,
)
def update_movie_slug(
    movie: MovieBySlug,
    movie_in: MovieUpdate,
) -> Movie:
    return storage.update(
        movie=movie,
        movie_in=movie_in,
    )


@router.patch(
    "/",
    response_model=MovieRead,
)
def update_movie_partial(
    movie: MovieBySlug,
    movie_in: MoviePartialUpdate,
) -> Movie:
    return storage.update_partial(
        movie=movie,
        movie_in=movie_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    slug: MovieBySlug,
) -> None:
    storage.delete(movie=slug)
