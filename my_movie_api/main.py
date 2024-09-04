from api.routes import router as movie_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(movie_router)
