from unittest import TestCase

from schemas.movie_url import Movie, MovieCreate


class MovieSchemaTestCase(TestCase):
    def test_movie_can_be_created_from_create_schema(self) -> None:
        movie_in = MovieCreate(
            slug="some-slug",
            title="some-title",
            year=2026,
            description="some-description",
            genre="some-genre",
        )
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.assertEqual(
            movie_in.slug,
            movie.slug,
        )
        self.assertEqual(
            movie_in.title,
            movie.title,
        )
        self.assertEqual(
            movie_in.year,
            movie.year,
        )
        self.assertEqual(
            movie_in.description,
            movie.description,
        )
        self.assertEqual(
            movie_in.genre,
            movie.genre,
        )
