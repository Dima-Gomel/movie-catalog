from fastapi import APIRouter

from .crud import MOVIES
from schemas.movie_url import Movie

router = APIRouter(
    prefix="/movies",
)


@router.get(
    "/",
    response_model=list[Movie],
)
def read_movie_details():
    return MOVIES
