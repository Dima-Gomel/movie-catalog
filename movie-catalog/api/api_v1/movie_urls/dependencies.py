from fastapi import APIRouter, HTTPException

from .crud import MOVIES

router = APIRouter()


@router.get("/movies_id/")
def read_movie_id(movie_id: int):
    for movie in MOVIES:
        if movie.movie_id == movie_id:
            return movie

    raise HTTPException(status_code=404, detail="Movie not found")
