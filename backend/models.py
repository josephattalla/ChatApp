from pydantic import BaseModel
from datetime import datetime


class Chat(BaseModel):
    chat_id: int
    room_id: int
    user_id: int
    message: str
    time: datetime


class Room(BaseModel):
    room_id: int
    room_name: str


class User(BaseModel):
    user_id: int
    username: str
    role: str
    hashed_password: str
