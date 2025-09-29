from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi.params import Depends
from starlette import status

from api.api_v1.movie_urls.crud import storage
from schemas.movie_url import Movie


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


@router.get(
    "/",
)
def read_movie_slug(slug: str) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug=slug)

    if movie:
        return movie
    raise HTTPException(
        status_code=404,
        detail=f"Movie {slug!r} not found",
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    slug: Annotated[
        Movie,
        Depends(read_movie_slug),
    ],
) -> None:
    storage.delete(movie=slug)
