from fastapi import APIRouter, HTTPException

from schemas.movie_url import Movie
from .crud import storage

router = APIRouter()


@router.get("/movie_slug/")
def read_movie_slug(slug: str) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug=slug)

    if movie:
        return movie
    raise HTTPException(
        status_code=404,
        detail=f"Movie {slug!r} not found",
    )
