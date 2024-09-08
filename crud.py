from typing import Any, Dict, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.db_movie import Movie as MovieModel
from models.movie import Movie


def get_movies(db: Session) -> List[MovieModel]:
    return db.query(MovieModel).all()


def get_movie_by_id(db: Session, movie_id: int) -> List[MovieModel]:
    return db.query(MovieModel).filter(MovieModel.id == movie_id).first()


def get_movie_by_category(db: Session, movie_category: str | None) -> List[MovieModel]:
    return db.query(MovieModel).filter(MovieModel.category == movie_category).all()


def create_movie(db: Session, movie: Movie) -> Dict[str, Any]:
    new_movie = MovieModel(**movie.model_dump())

    db.add(new_movie)
    db.commit()

    movie_count = db.query(MovieModel).count()

    response_data: Dict[str, Any] = {
        "message": "The movie has been created",
        "metadata": {"count": movie_count},
    }

    return response_data


def update_movie(db: Session, movie_id: int, updated_data: Movie) -> Dict[str, Any]:
    if movie_id and get_movie_by_id(db, movie_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )

    movie = get_movie_by_id(db, movie_id)

    updated_movie = updated_data.model_dump()

    for key, value in updated_movie.items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)

    response_data: Dict[str, Any] = {
        "message": "The movies has been updated correctly",
        "data": movie,
    }
    return response_data


def patched_movie(db: Session, movie_id: int, updated_data: Movie) -> Dict[str, Any]:
    movie = get_movie_by_id(db, movie_id)
    if movie_id and movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )

    updated_movie = updated_data.model_dump(exclude_unset=True)

    for key, value in updated_movie.items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)

    response_data: Dict[str, Any] = {
        "message": "The movies has been patched correctly",
        "data": Movie.model_validate(movie),
    }
    return response_data


def delete_movie(db: Session, movie_id):
    movie = get_movie_by_id(db, movie_id)
    if movie_id and movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )

    db.delete(movie)
    db.commit()

    movie_count = db.query(MovieModel).count()

    response_data: Dict[str, Any] = {
        "message": "The movie has been created",
        "metadata": {"count": movie_count},
    }

    return response_data
