from pydantic import BaseModel
from typing_extensions import Annotated

Annotation = Annotated[str, ""]


class MovieBase(BaseModel):
    """
    Базовый класс
    """

    title: Annotation
    year: Annotated[int, ""]
    description: Annotation
    genre: Annotation


class MovieCreate(MovieBase):
    """Модель для создания фильма"""

    slug: Annotation


class MovieUpdate(MovieBase):
    """
    Модель обновления фильма
    """


class MoviePartialUpdate(MovieBase):
    """
    Модель для частичного обновления фильма
    """

    title: Annotation | None = None
    year: Annotated[int, ""] | None = None
    description: Annotation | None = None
    genre: Annotation | None = None


class Movie(MovieBase):
    """
    Модель фильма
    """

    slug: str
    title: str
    year: int
    description: str
    genre: str
