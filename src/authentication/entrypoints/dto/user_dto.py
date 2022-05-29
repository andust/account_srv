from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: Optional[int]
    full_name: str = Field(..., min_length=2, max_length=128)
    email: EmailStr | str


class UserCreate(User):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
