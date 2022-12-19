from typing import Union
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
	first_name:str
	last_name:str
	email:EmailStr


class UserForm(UserBase):
	pass


class UserValidate(UserBase):
	hashed_password: str
	is_active: str


class User(UserBase):
	id: int
	is_active: bool

	class Config:
		orm_mode = True