from fastapi import FastAPI
from pydantic import BaseModel

class Chat(BaseModel):
    chat_id: int
    room_id: int
    user_id: int
    message: str
    time: str

class Rooms(BaseModel):
    room_id: int
    room_name: str

class Users(BaseModel):
    user_id: int
    username: str
    hash_pass: str

app = FastAPI()