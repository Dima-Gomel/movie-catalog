from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from schemas.movie_url import (
    Movie,
    MovieCreate,
    MovieRead,
)

from api.api_v1.movie_urls.crud import MovieAlreadyExistsError, storage
from api.api_v1.movie_urls.dependencies import (
    api_token_or_url_required_for_unsafe_methods,
)
from api.api_v1.movie_urls.views.details_views import router as detail_router

router = APIRouter(
    prefix="/movies",
    dependencies=[
        Depends(api_token_or_url_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token!!!",
                    },
                },
            },
        },
    },
)

router.include_router(detail_router)


@router.get(
    "/",
    response_model=list[MovieRead],
)
def read_movie_details() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "A movie with the same name slug already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug='name' already exists.",
                    }
                }
            },
        }
    },
)
def create_movie(
    movie_create: MovieCreate,
) -> Movie:
    try:
        return storage.create_or_raise_if_exists(movie_create)

    except MovieAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Movie with slug={movie_create.slug!r} already exists.",
        )
