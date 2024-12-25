from pydantic import BaseModel, Field


class ReviewForm(BaseModel):
    rating: int = Field(ge=1, le=10)
    text: str = Field(..., max_length=255)
