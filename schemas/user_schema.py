from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    age: Optional[int] = None

class UserSignup(BaseModel):
    name: str
    email: str
    password: str
    age: int

class UserLogin(BaseModel):
    email: str
    password: str

class Config:
        from_attributes = True