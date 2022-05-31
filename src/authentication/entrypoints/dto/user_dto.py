from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserEmail(BaseModel):
    email: EmailStr | str

class User(UserEmail):
    id: Optional[int]
    full_name: str = Field(..., min_length=2, max_length=128)
    

class UserCredentials(BaseModel):
    email: EmailStr | str
    password: str = Field(..., min_length=8, max_length=128)

class UserCreate(User, UserCredentials):
    ...
