from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: int | None = None
    title: str = Field(min_length=2, max_length=15)
    overview: str = Field(min_length=2, max_length=100)
    year: int = Field(le=2024)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=2, max_length=15)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "My movie",
                "overview": "Movie overview",
                "year": 2024,
                "rating": 0.0,
                "category": "action",
            }
        }
    }
