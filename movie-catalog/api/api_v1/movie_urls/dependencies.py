from fastapi import APIRouter, HTTPException

from .crud import MOVIES

router = APIRouter()


@router.get("/movie_slug/")
def read_movie_id(slug: str):
    for movie in MOVIES:
        if movie.slug == slug:
            return movie

    raise HTTPException(status_code=404, detail="Movie not found")
