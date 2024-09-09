from fastapi import FastAPI

from api.routes import router as movie_router
from middlewares.error_handler import ErrorHandler

app = FastAPI()
app.title = "Movie FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

app.include_router(movie_router)
