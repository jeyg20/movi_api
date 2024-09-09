from typing import Annotated, Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

import crud
from auth.jwt_manager import create_token
from config.database import Base, SessionLocal, engine
from models.db_movie import Movie as MovieModel
from models.jwt_bearer import JWTBearer
from models.movie import Movie
from models.user import User

router: APIRouter = APIRouter()

Base.metadata.create_all(bind=engine)

movies = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


@router.post(
    "/login",
    tags=["auth"],
    status_code=status.HTTP_200_OK,
)
@router.post("/login", tags=["auth"])
async def login(user: User) -> str:
    if not user.email == "admin@gmail.com" and user.password == "admin":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalied email or password",
        )

    token: str = create_token(user.model_dump())
    return token


@router.get(
    "/movies",
    tags=["movies"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
async def get_movies(db: Session = Depends(get_db)):
    result = crud.get_movies(db)
    return result


@router.get(
    "/movies/{movie_id}",
    tags=["movies"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
async def get_movie_by_id(
    movie_id: Annotated[int, Path(ge=0, le=999)], db: Session = Depends(get_db)
):
    db_movie = crud.get_movie_by_id(db, movie_id)

    if db_movie is None:
        error_response = f"The movie with id {movie_id}, does not exist"
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response,
        )
    return db_movie


@router.get(
    "/movies/",
    tags=["movies"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
async def get_movies_by_category(
    category: Annotated[str | None, Query(min_length=5, max_length=15)] = None,
    db: Session = Depends(get_db),
):
    filtered_movies = crud.get_movie_by_category(db, category)
    if not filtered_movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found matching the criteria.",
        )
    return filtered_movies


@router.post(
    "/movies",
    tags=["movies"],
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    dependencies=[Depends(JWTBearer())],
)
async def create_movie(movie: Movie, db: Session = Depends(get_db)) -> Dict[str, Any]:

    if movie.id and crud.get_movie_by_id(db, movie.id):
        error_response = f"A movie with id {movie.id}, already exists"
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_response,
        )

    new_movie = crud.create_movie(db, movie)

    return new_movie


@router.post(
    "/movies/batch",
    tags=["movies"],
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    dependencies=[Depends(JWTBearer())],
)
async def create_multiple_movies(
    movies: List[Movie] | Movie, db: Session = Depends(get_db)
) -> Dict[str, Any]:

    if isinstance(movies, Movie):
        movies = [movies]

    for movie in movies:
        if movie.id and crud.get_movie_by_id(db, movie.id):
            error_response = f"A movie with id {movie.id}, already exists"
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_response,
            )
        new_movie = crud.create_movie(db, movie)

    return new_movie


@router.put(
    "/movies/{movie_id}",
    tags=["movies"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
async def update_movie(
    movie_id: Annotated[int, Path(ge=0, le=999)],
    updated_data: Movie,
    db: Session = Depends(get_db),
):
    updated_movie = crud.update_movie(db, movie_id, updated_data)
    return updated_movie


@router.delete(
    "/movies/{movie_id}",
    tags=["movies"],
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())],
)
async def delete_movie(
    movie_id: Annotated[int, Path(ge=0, le=999)],
    db: Session = Depends(get_db),
):
    delted_movie = crud.delete_movie(db, movie_id)
    return delted_movie
