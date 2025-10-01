from fastapi import HTTPException
from starlette import status

from .crud import storage
from schemas.movie_url import Movie


def prefetch_movie(slug: str) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug=slug)

    if movie:
        return movie
    raise HTTPException(
        status_code=404,
        detail=f"Movie {slug!r} not found",
    )
