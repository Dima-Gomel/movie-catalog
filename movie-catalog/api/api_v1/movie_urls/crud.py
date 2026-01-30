"""
Create - создание
Read - чтение
Update - обновление
Delete - удаление
"""

import logging

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from schemas.movie_url import (
    Movie,
    MovieUpdate,
    MoviePartialUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIE,
    decode_responses=True,
)


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
            for values in redis.hvals(name=config.REDIS_MOVIE_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        if data := redis.hget(
            name=config.REDIS_MOVIE_HASH_NAME,
            key=slug,
        ):
            return Movie.model_validate_json(data)

    def create(
        self,
        movie_create: Movie,
    ) -> Movie:
        movie_create = Movie(
            **movie_create.model_dump(),
        )
        self.save_movie(movie_create)
        log.info("Create Movie %s", movie_create)
        return movie_create

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
