from unittest import TestCase

from pydantic import ValidationError
from schemas.movie_url import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)


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

    def test_with_different_movie_data(self) -> None:
        test_cases = [
            {
                "name": "Стандартный фильм",
                "data": {
                    "slug": "matritsa-1999",
                    "title": "Матрица",
                    "year": 1999,
                    "description": "Культовый фантастический фильм братьев Вачовски",
                    "genre": "Фантастика",
                },
            },
            {
                "name": "Фильм с длинным названием",
                "data": {
                    "slug": "priklyucheniya-sherloka-holmsa-i-doktora-vatsona",
                    "title": "Приключения Шерлока Холмса и доктора Ватсона",
                    "year": 1980,
                    "description": "Советский телевизионный фильм",
                    "genre": "Детектив",
                },
            },
            {
                "name": "Фильм с пустым описанием",
                "data": {
                    "slug": "empty-description",
                    "title": "Фильм без описания",
                    "year": 2024,
                    "description": "",
                    "genre": "Драма",
                },
            },
            {
                "name": "Фильм с очень длинным описанием",
                "data": {
                    "slug": "long-description",
                    "title": "Фильм с длинным описанием",
                    "year": 2023,
                    "description": "Это очень длинное описание фильма. " * 50,
                    "genre": "Триллер",
                },
            },
            {
                "name": "Фильм с годом в прошлом",
                "data": {
                    "slug": "starina-1920",
                    "title": "Старина",
                    "year": 1920,
                    "description": "Немое кино",
                    "genre": "Исторический",
                },
            },
            {
                "name": "Фильм с будущим годом",
                "data": {
                    "slug": "buduschee-3000",
                    "title": "Будущее",
                    "year": 3000,
                    "description": "Фильм о далеком будущем",
                    "genre": "Фантастика",
                },
            },
            {
                "name": "Фильм со специальными символами в полях",
                "data": {
                    "slug": "special-chars-123",
                    "title": "Фильм #1: Спецсимволы!",
                    "year": 2024,
                    "description": "Описание с !@#$%^&*() символами",
                    "genre": "Sci-Fi/Хоррор",
                },
            },
            {
                "name": "Фильм с минимальными данными",
                "data": {
                    "slug": "min",
                    "title": "Мин",
                    "year": 2000,
                    "description": "Мин",
                    "genre": "Мин",
                },
            },
        ]

        for case in test_cases:
            with self.subTest(case["name"]):
                # Создаем схему с тестовыми данными
                movie_in = MovieCreate(**case["data"])

                # Создаем экземпляр Movie из схемы
                movie = Movie(**movie_in.model_dump())

                # Проверяем все поля
                self.assertEqual(movie_in.slug, movie.slug)
                self.assertEqual(movie_in.title, movie.title)
                self.assertEqual(movie_in.year, movie.year)
                self.assertEqual(movie_in.description, movie.description)
                self.assertEqual(movie_in.genre, movie.genre)

                # Дополнительные проверки для description
                self.assertEqual(
                    len(movie.description),
                    len(case["data"]["description"]),
                )

    def test_movie_slug_too_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            MovieCreate(
                slug="s",
                title="some-title",
                year=2026,
                description="some-description",
                genre="some-genre",
            )

        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_short"
        self.assertEqual(
            expected_type,
            error_details["type"],
        )

    def test_movie_slug_too_short_with_regex(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at least 3 characters",
        ):
            MovieCreate(
                slug="s",
                title="some-title",
                year=2026,
                description="some-description",
                genre="some-genre",
            )


class MovieUpdateTestCase(TestCase):
    def test_movie_can_be_created_from_update_schema(self) -> None:
        movie_in = MovieUpdate(
            title="some-title",
            year=2026,
            description="some-description",
            genre="some-genre",
        )
        movie = Movie(
            slug="some-slug",
            **movie_in.model_dump(),
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


class MoviePartialUpdateTestCase(TestCase):
    def test_movie_can_be_created_from_partial_update_schema(self) -> None:
        movie_in = MoviePartialUpdate(
            title="some-title",
            year=2026,
            description="some-description",
            genre="some-genre",
        )
        movie = Movie(
            slug="some-slug",
            **movie_in.model_dump(),
        )
        self.assertEqual(
            movie_in.title or None,
            movie.title,
        )
        self.assertEqual(
            movie_in.year or None,
            movie.year,
        )
        self.assertEqual(
            movie_in.description or None,
            movie.description,
        )
        self.assertEqual(
            movie_in.genre or None,
            movie.genre,
        )
