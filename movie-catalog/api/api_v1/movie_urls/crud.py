"""
Create - создание
Read - чтение
Update - обновление
Delete - удаление
"""

__all__ = ("storage",)

import logging
from collections.abc import Iterable
from typing import cast

from core import config
from pydantic import BaseModel
from redis import Redis
from schemas.movie_url import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIE,
    decode_responses=True,
)


class MovieBaseError(Exception):
    """
    Base exception for movie CRUD actions.
    """


class MovieAlreadyExistsError(MovieBaseError):
    """
    Raised on movie creation if such slug already exists.
    """


class MovieStorage(BaseModel):
    slug_to_movie_storage: dict[str, Movie] = {}

    def save_movie(self, movie: Movie) -> None:
        redis.hset(
            name=config.REDIS_MOVIE_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(values)
            for values in cast(
                Iterable[str],
                redis.hvals(name=config.REDIS_MOVIE_HASH_NAME),
            )
        ]

    def exists(self, slug: str) -> bool:
        return bool(
            redis.hexists(
                name=config.REDIS_MOVIE_HASH_NAME,
                key=slug,
            ),
        )

    def get_by_slug(self, slug: str) -> Movie | None:
        if data := redis.hget(
            name=config.REDIS_MOVIE_HASH_NAME,
            key=slug,
        ):
            assert isinstance(data, str)
            return Movie.model_validate_json(data)

        return None

    def create(
        self,
        movie_create: MovieCreate,
    ) -> Movie:
        movie = Movie(
            **movie_create.model_dump(),
        )
        self.save_movie(movie)
        log.info("Create Movie %s", movie)
        return movie

    def create_or_raise_if_exists(self, movie_create: MovieCreate) -> Movie:
        if not self.get_by_slug(movie_create.slug):
            return self.create(movie_create)
        raise MovieAlreadyExistsError(movie_create.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(
            config.REDIS_MOVIE_HASH_NAME,
            slug,
        )

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_movie(movie)
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MoviePartialUpdate,
    ) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_movie(movie)
        return movie


storage = MovieStorage()
