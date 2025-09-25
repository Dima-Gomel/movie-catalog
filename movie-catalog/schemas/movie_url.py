from pydantic import BaseModel
from typing_extensions import Annotated


class MovieBase(BaseModel):
    """
    Базовый класс
    """


class Movie(MovieBase):
    """
    Модель фильма
    """

    slug: Annotated[str, ""]
    title: Annotated[str, ""]
    year: Annotated[int, ""]
    description: Annotated[str, ""]
    genre: Annotated[str, ""]
