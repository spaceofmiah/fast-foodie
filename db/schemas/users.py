from typing import Union
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
	first_name:str
	last_name:str
	email:EmailStr


class UserCreate(UserBase):
	hashed_password: str = Field(
		alias="password",
		min_length=8
	)


class User(UserBase):
	id: int
	is_active: bool

	class Config:
		orm_mode = True