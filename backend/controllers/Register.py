from typing import Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pydantic.types import StringConstraints

from ..utils.auth import UserInDB, fake_users_db, get_password_hash


class RegisterUser(BaseModel):
    username: Annotated[
        str,
        StringConstraints(
            min_length=4,
            max_length=20,
        ),
    ]
    password: Annotated[
        str,
        StringConstraints(
            min_length=8,
            max_length=20,
        ),
    ]


router = APIRouter()


# TODO: implement with actual DB
@router.post("/register", status_code=201)
def register(registerData: RegisterUser):
    # check if username already in use
    if registerData.username in fake_users_db:
        raise HTTPException(status_code=409, detail="Username already in use.")

    # hash password
    hash_pass = get_password_hash(registerData.password)

    # add to DB
    user = UserInDB(
        username=registerData.username,
        hashed_password=hash_pass,
        user_id=1,
    )
    fake_users_db[user.username] = user.model_dump()

    return
