import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    Header,
    status,
)
from fastapi.params import Depends

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from core.config import API_TOKENS
from .crud import storage
from schemas.movie_url import Movie

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)

static_api_token = HTTPBearer(
    scheme_name="Static API token ",
    description="Your **Static API token** from the developer portal. [Read more](#)",
    auto_error=False,
)


def prefetch_movie(slug: str) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug=slug)

    if movie:
        return movie
    raise HTTPException(
        status_code=404,
        detail=f"Movie {slug!r} not found",
    )


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
):
    log.info("incoming %r request", request.method)
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to save storage")
        background_tasks.add_task(storage.save_state)


def api_token_required(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
