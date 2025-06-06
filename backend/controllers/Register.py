from fastapi import APIRouter
from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    password: str


router = APIRouter()


@router.post("/register", status_code=201)
def register(registerData: RegisterUser):
    # 1. validate username & password
    # 2. hash password
    # 3. add to DB
    return
