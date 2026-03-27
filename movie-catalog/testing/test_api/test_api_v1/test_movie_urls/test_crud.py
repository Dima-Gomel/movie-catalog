import random
import string
from collections.abc import Generator
from typing import (
    ClassVar,
)
from unittest import TestCase

import pytest
from api.api_v1.movie_urls.crud import (
    MovieAlreadyExistsError,
    storage,
)
from schemas.movie_url import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)


def create_movie() -> Movie:
    movie_in = MovieCreate(
        slug="".join(
            random.choices(
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


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def test_update(self) -> None:
        movie_update = MovieUpdate(
            **self.movie.model_dump(),
        )
        source_description = self.movie.description
        movie_update.description *= 2
        updated_movie = storage.update(
            movie=self.movie,
            movie_in=movie_update,
        )
        self.assertNotEqual(
            source_description,
            updated_movie.description,
        )
        self.assertEqual(
            movie_update,
            MovieUpdate(**movie_update.model_dump()),
        )

    def test_update_partial(self) -> None:
        movie_partial_update = MoviePartialUpdate(
            description=self.movie.description * 2,
        )
        source_description = self.movie.description
        updated_movie = storage.update_partial(
            movie=self.movie,
            movie_in=movie_partial_update,
        )
        self.assertNotEqual(
            source_description,
            updated_movie.description,
        )
        self.assertEqual(
            movie_partial_update.description,
            updated_movie.description,
        )


class MovieStorageGetMovieTestCase(TestCase):
    MOVIE_COUNT = 3
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie() for _ in range(cls.MOVIE_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        movies = storage.get()
        expected_slug = {m.slug for m in self.movies}
        slugs = {m.slug for m in movies}
        expected_diff = set[str]()
        diff = expected_slug - slugs
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                slug=movie.slug,
                msg=f"Valideate can get slug {movie.slug}!r",
            ):
                db_movie = storage.get_by_slug(movie.slug)
                self.assertEqual(
                    movie,
                    db_movie,
                )


def test_create_or_raise_if_exists(movie: Movie) -> None:
    movie_create = MovieCreate(**movie.model_dump())
    with pytest.raises(
        MovieAlreadyExistsError,
        match=movie_create.slug,
    ) as exp_info:
        storage.create_or_raise_if_exists(movie_create)

    assert exp_info.value.args[0] == movie_create.slug
