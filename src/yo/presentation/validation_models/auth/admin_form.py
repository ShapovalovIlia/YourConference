from pydantic import BaseModel, Field, field_validator


class AdminForm(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=5)

    @field_validator("username")
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError("Username should be alphanumeric")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 5:
            raise ValueError("Password must be at least 8 characters long")
        return v
