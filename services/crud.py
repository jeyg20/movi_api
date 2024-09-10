from typing import Any, Dict, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.db_movie import Movie as MovieModel
from models.movie import Movie


class MovieServices:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_movies(self) -> List[MovieModel]:
        return self.db.query(MovieModel).all()

    def get_movie_by_id(self, movie_id: int) -> MovieModel:
        return self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    def get_movie_by_category(self, movie_category: str | None) -> List[MovieModel]:
        return (
            self.db.query(MovieModel)
            .filter(MovieModel.category == movie_category)
            .all()
        )

    def create_movie(self, movie: Movie) -> Dict[str, Any]:
        new_movie = MovieModel(**movie.model_dump())

        self.db.add(new_movie)
        self.db.commit()

        movie_count = self.db.query(MovieModel).count()

        response_data: Dict[str, Any] = {
            "message": "The movie has been created",
            "metadata": {"count": movie_count},
        }

        return response_data

    def update_movie(self, movie_id: int, updated_data: Movie) -> Dict[str, Any]:
        movie = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()

        if movie is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
            )

        updated_movie = updated_data.model_dump(exclude_unset=True)

        for key, value in updated_movie.items():
            setattr(movie, key, value)

        self.db.commit()
        self.db.refresh(movie)

        response_data: Dict[str, Any] = {
            "message": "The movie has been updated correctly",
            "data": movie,
        }
        return response_data

    def delete_movie(self, movie_id):
        movie = self.db.query(MovieModel).filter(MovieModel.id == movie_id).first()
        if movie_id and movie is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
            )

        self.db.delete(movie)
        self.db.commit()

        movie_count = self.db.query(MovieModel).count()

        response_data: Dict[str, Any] = {
            "message": "The movie has been created",
            "metadata": {"count": movie_count},
        }

        return response_data
