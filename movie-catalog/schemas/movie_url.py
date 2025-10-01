from pydantic import BaseModel
from typing_extensions import Annotated


class MovieBase(BaseModel):
    """
    Базовый класс
    """


class MovieCreate(MovieBase):
    """Модель для создания фильма"""

    slug: Annotated[str, ""]


class MovieUpdate(MovieBase):
    """
    Модель обновления фильма
    """

    title: Annotated[str, ""]
    year: Annotated[int, ""]
    description: Annotated[str, ""]
    genre: Annotated[str, ""]


class Movie(MovieBase):
    """
    Модель фильма
    """

    slug: str
    title: str
    year: int
    description: str
    genre: str
