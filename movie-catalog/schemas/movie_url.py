from typing import Annotated

from annotated_types import (
    Len,
    MaxLen,
)
from pydantic import BaseModel

DescriptionString = Annotated[
    str,
    MaxLen(200),
]


class MovieBase(BaseModel):
    """
    Базовый класс
    """

    title: DescriptionString
    year: Annotated[int, ""]
    description: DescriptionString
    genre: DescriptionString


class MovieCreate(MovieBase):
    """
    Модель для создания фильма
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]


class MovieUpdate(MovieBase):
    """
    Модель обновления фильма
    """


class MoviePartialUpdate(BaseModel):
    """
    Модель для частичного обновления фильма
    """

    title: DescriptionString | None = None
    year: Annotated[int, ""] | None = None
    description: DescriptionString | None = None
    genre: DescriptionString | None = None


class MovieRead(MovieBase):
    """
    Модель для чтения данных о записи с фильмом
    """

    slug: str


class Movie(MovieBase):
    """
    Модель фильма
    """

    slug: str
    title: str
    year: int
    description: str
    genre: str
    notes: str = "Dima"
