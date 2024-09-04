from typing import Annotated, Any, Dict, List

from fastapi import APIRouter, HTTPException, Path, Query, status
from fastapi.responses import HTMLResponse
from models.movie import Movie

router: APIRouter = APIRouter()

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


def find_movie_by_id(movie_id: int) -> Movie:
    movie = next((item for item in movies if item.id == movie_id), None)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    return movie


@router.get("/", tags=["home"])
async def message():
    return HTMLResponse("<h1>Hello user!</h1>")


@router.get(
    "/movies",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
)
async def get_movies():
    return movies


@router.get(
    "/movies/{movie_id}",
    tags=["movies"],
    response_model=Movie,
    status_code=status.HTTP_200_OK,
)
async def get_movie(movie_id: Annotated[int, Path(ge=0, le=999)]):
    return find_movie_by_id(movie_id)


@router.get(
    "/movies/",
    tags=["movies"],
    response_model=List[Movie],
    status_code=status.HTTP_200_OK,
)
async def get_movies_by_category(
    category: Annotated[str | None, Query(min_length=5, max_length=15)] = None,
    year: Annotated[int | None, Query(ge=0, le=2024)] = None,
):
    filtered_movies = [
        item
        for item in movies
        if (category is None or category == item.category)
        and (year is None or year == item.year)
    ]
    if not filtered_movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found matching the criteria.",
        )
    return filtered_movies


@router.post(
    "/movies",
    tags=["movies"],
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
)
async def create_movie(movie: Movie):
    if any(existing_movie.id == movie.id for existing_movie in movies):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie with this ID already exists.",
        )
    movies.append(movie)
    response_data: Dict[str, Any] = {
        "message": "The movie has been created",
        "metadate": {"count": len(movies)},
        "data": movie,
    }
    return response_data


@router.put(
    "/movies/{movie_id}",
    tags=["movies"],
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def update_movie(
    movie_id: Annotated[int, Path(ge=0, le=999)], movie_update: Movie
):
    if find_movie_by_id(movie_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    movies[movie_id] = movie_update
    response_data: Dict[str, Any] = {
        "message": "The movies has been updated correctly",
        "data": movie_update,
    }
    return response_data


@router.patch(
    "/movies/{movie_id}",
    tags=["movies"],
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def patch_movie(
    movie_id: Annotated[int, Path(ge=0, le=999)], movie_update: Movie
):
    if find_movie_by_id(movie_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )

    stored_movie = movies[movie_id]
    update_data = movie_update.model_dump(exclude_unset=True)
    updated_movie = stored_movie.model_copy(update=update_data)

    movies[movie_id] = updated_movie

    response_data: Dict[str, Any] = {
        "message": "The movies has been updated correctly",
        "data": updated_movie,
    }
    return response_data


@router.delete(
    "/movies/{movie_id}",
    tags=["movies"],
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def delete_movie(movie_id: Annotated[int, Path(ge=0, le=999)]):
    if find_movie_by_id(movie_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    movies.pop(movie_id)

    response_data: Dict[str, Any] = {
        "message": f"The movie with id {movie_id} has been deleted",
        "metadate": {"count": len(movies)},
    }
    return response_data
