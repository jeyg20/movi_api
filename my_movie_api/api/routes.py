from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from models.movie import Movie, MovieUpdate

router = APIRouter()

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


@router.get("/", tags=["home"])
async def message():
    return HTMLResponse("<h1>Hello user!</h1>")


@router.get("/movies", tags=["movies"])
async def get_movies():
    return movies


@router.get("/movies/{id}", tags=["movies"])
async def get_movie(id: int):
    movie = next((item for item in movies if item.id == id), None)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@router.get("/movies/search", tags=["movies"])
async def get_movies_by_category(
    category: Optional[str] = None, year: Optional[int] = None
):
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


@router.post("/movies", tags=["movies"])
async def create_movie(movie: Movie):
    if any(existing_movie.id == movie.id for existing_movie in movies):
        raise HTTPException(
            status_code=400, detail="Movie with this ID already exists."
        )
    movies.append(movie)
    return movie


@router.put("/movies/{item_id}", tags=["movies"])
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


@router.delete("/movies/{item_id}", tags=["movies"])
async def delete_movie(item_id: int):
    index = next((i for i, item in enumerate(movies) if item.id == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movies.pop(index)
    return {"message": f"Movie with id {item_id} was deleted"}
