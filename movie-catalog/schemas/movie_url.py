from pydantic import BaseModel
from typing_extensions import Annotated


class MovieBase(BaseModel):
    """
    Базовый класс
    """


class MovieCreate(MovieBase):
    title: Annotated[str, ""]
    year: Annotated[int, ""]
    description: Annotated[str, ""]
    genre: Annotated[str, ""]


class Movie(MovieBase):
    """
    Модель фильма
    """

    movie_id: int
