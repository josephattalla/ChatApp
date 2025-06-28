from typing import Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pydantic.types import StringConstraints

from ..utils.auth import get_password_hash
from ..db_functions import addUser, findUserWithUsername


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


@router.post("/register", status_code=201)
def register(registerData: RegisterUser):
    # check if username already in use
    if findUserWithUsername("Admin", registerData.username):
        raise HTTPException(status_code=409, detail="Username already in use.")

    # hash password
    hash_pass = get_password_hash(registerData.password)

    # add to DB
    addedUser = addUser("Admin", registerData.username, hash_pass)

    if not addedUser:
        raise HTTPException(status_code=400)

    del addedUser.hashed_password

    return addedUser
