from pydantic import BaseModel


class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str


class MovieUpdate(BaseModel):
    title: str | None = None
    overview: str | None = None
    year: int | None = None
    rating: float | None = None
    category: str | None = None
