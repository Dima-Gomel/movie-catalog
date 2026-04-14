import random
import string
from collections.abc import Generator
from os import getenv

import pytest
from api.api_v1.movie_urls.crud import storage
from schemas.movie_url import Movie, MovieCreate

if getenv("TESTING") != "1":
    pytest.exit(
        "Environment is not ready for testing",
    )


def create_movie() -> Movie:
    movie_in = MovieCreate(
        slug="".join(
            random.choices(  # noqa: S311
                string.ascii_letters,
                k=8,
            ),
        ),
        title="A movie title",
        year=2000,
        description="A movie description",
        genre="A movie genre",
    )
    return storage.create(movie_in)


@pytest.fixture()
def movie() -> Generator[Movie]:
    movie_create = create_movie()
    yield movie_create
    storage.delete(movie_create)
