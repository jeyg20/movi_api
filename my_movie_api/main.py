from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app: FastAPI = FastAPI()
app.title = "My app with FastAPI"
app.version = "0.0.1"


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


movies: List[Movie] = [
    Movie(
        id=0,
        title="Avatar",
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year=2009,
        rating=7.8,
        category="action",
    ),
    Movie(
        id=1,
        title="Avatar 2",
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year=2022,
        rating=7.8,
        category="adventure",
    ),
]


@app.get("/", tags=["home"])
async def message():
    return HTMLResponse("<h1>Hello user!</h1>")


@app.get("/movies", tags=["movies"])
async def get_movies():
    return movies


@app.get("/movies/{id}", tags=["movies"])
async def get_movie(id: int):
    movie = next((item for item in movies if item.id == id), None)
    if movie is None:
        raise HTTPException(status_code=404, detail="Moview was not found")
    return movie


@app.get("/movies/", tags=["movies"])
async def get_movies_by_category(category: str | None = None, year: int | None = None):
    filtered_movies = [
        item
        for item in movies
        if (category is None or item.category.lower() == category.lower())
        and (year is None or item.year == year)
    ]

    if not filtered_movies:
        raise HTTPException(
            status_code=404, detail="No movies found matching the criteria."
        )

    return filtered_movies


@app.post("/movies", tags=["movies"])
async def create_movie(movie: Movie):
    if any(existing_movie.id == movie.id for existing_movie in movies):
        raise HTTPException(
            status_code=400, detail="Movie with this ID already exists."
        )

    movies.append(movie)

    return movie.title


@app.put("/movies/{item_id}", tags=["movies"])
async def update_movie(item_id: int, movie_update: MovieUpdate):
    index = next((i for i, item in enumerate(movies) if item.id == item_id), None)

    if index is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    updated_movie = movies[index]
    if movie_update.title is not None:
        updated_movie.title = movie_update.title

    if movie_update.overview is not None:
        updated_movie.overview = movie_update.overview

    if movie_update.year is not None:
        updated_movie.year = movie_update.year

    if movie_update.rating is not None:
        if not (0.0 <= movie_update.rating <= 10.0):
            raise HTTPException(
                status_code=400, detail="Rating must be between 0.0 and 10.0"
            )
        updated_movie.rating = movie_update.rating

    if movie_update.category is not None:
        updated_movie.category = movie_update.category

    movies[index] = updated_movie

    return updated_movie


@app.delete("/movies/{item_id}", tags=["movies"])
async def delete_movie(item_id: int):
    index = next((i for i, item in enumerate(movies) if item.id == item_id), None)

    if index is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    movies.pop(index)
    return {"message": f"Movie with id {item_id} was deleted"}
