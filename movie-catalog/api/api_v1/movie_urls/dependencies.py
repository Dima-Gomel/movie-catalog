import logging

from fastapi import HTTPException, BackgroundTasks

from .crud import storage
from schemas.movie_url import Movie

log = logging.getLogger(__name__)


def prefetch_movie(slug: str) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug=slug)

    if movie:
        return movie
    raise HTTPException(
        status_code=404,
        detail=f"Movie {slug!r} not found",
    )


def save_storage_state(
    background_tasks: BackgroundTasks,
):

    yield
    log.info("Add background task to save storage")
    background_tasks.add_task(storage.save_state)
