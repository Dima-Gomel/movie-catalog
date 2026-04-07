import random
import string

from fastapi import status
from main import app
from schemas.movie_url import MovieCreate
from starlette.testclient import TestClient


def test_create_movie(auth_client: TestClient) -> None:
    url = app.url_path_for("create_movie")
    movie_create = MovieCreate(
        slug="".join(
            random.choices(  # nosec B311  # noqa: S311
                string.ascii_letters,
                k=8,
            ),
        ),
        title="A movie title",
        year=2000,
        description="A movie description",
        genre="A movie genre",
    )
    data: dict[str, str] = movie_create.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = MovieCreate(**response_data)
    assert received_values == movie_create, response_data
