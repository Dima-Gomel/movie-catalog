from typing import Annotated

from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.movie_urls.crud import storage
from api.api_v1.movie_urls.dependencies import (
    prefetch_movie,
    api_token_required,
)

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
    _=Depends(api_token_required),
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
    _=Depends(api_token_required),
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
    movie: MovieBySlug,
    _=Depends(api_token_required),
) -> None:
    storage.delete(movie=movie)
