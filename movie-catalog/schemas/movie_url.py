from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    year: int
    description: str
    genre: str


class Movie(MovieBase):
    movie_id: int
