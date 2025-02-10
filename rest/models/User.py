from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base


class User(BaseModel):
    username: str
    password: str
    token: Optional[str]

    class Config:
        orm_mode = True


class UserModel(declarative_base()):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    password = Column(String)
    token = Column(String)
