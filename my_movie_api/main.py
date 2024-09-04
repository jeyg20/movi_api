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
    year: str
    rating: float
    category: str


movies: List[Movie] = [
    Movie(
        id=1,
        title="Avatar",
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year="2009",
        rating=7.8,
        category="Acción",
    ),
    Movie(
        id=2,
        title="Avatar 2",
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year="2020",
        rating=7.8,
        category="Acción",
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
