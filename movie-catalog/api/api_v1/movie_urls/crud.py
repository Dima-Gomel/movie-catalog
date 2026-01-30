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
from core.config import MOVIE_CATALOG_STORAGE_FILEPATH

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

    def save_state(self) -> None:
        MOVIE_CATALOG_STORAGE_FILEPATH.write_text(
            self.model_dump_json(indent=2), encoding="utf-8"
        )
        log.info("Saved movie to storage file.")

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIE_CATALOG_STORAGE_FILEPATH.exists():
            log.info("movie storage file doesn't exist.")
            return MovieStorage()
        return cls.model_validate_json(
            MOVIE_CATALOG_STORAGE_FILEPATH.read_text(encoding="utf-8")
        )

    def init_storage_from_state(self) -> None:
        try:
            data = MovieStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error.")
            return

        # мы обновляем свойства напрямую
        # если будут новые свойства
        # то их тоже надо обновить
        self.slug_to_movie_storage.update(
            data.slug_to_movie_storage,
        )
        log.warning("Recovered data from storage file.")

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
        # values = redis.hvals(config.REDIS_MOVIE_HASH_NAME)
        # movies = []
        # for value in values:
        #     movie = Movie.model_validate_json(value)
        #     movies.append(movie)
        # return movies

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
