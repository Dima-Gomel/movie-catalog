from fastapi import (
    status,
    APIRouter,
    Depends,
    HTTPException,
)

from api.api_v1.movie_urls.crud import storage
from api.api_v1.movie_urls.dependencies import (
    api_token_or_url_required_for_unsafe_methods,
)
from api.api_v1.movie_urls.views.details_views import router as detail_router

from schemas.movie_url import (
    Movie,
    MovieCreate,
    MovieRead,
)

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
def read_movie_details():
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_create: MovieCreate,
) -> Movie:
    if not storage.get_by_slug(movie_create.slug):
        return storage.create(movie_create)

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Movie with slug='foobar' already exists.",
    )
