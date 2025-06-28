from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated

from ..utils.auth import get_current_user, oauth2_scheme
from ..db_functions import addRoom

router = APIRouter()


@router.post("/room", status_code=201)
async def addNewRoom(
    token: Annotated[str, Depends(oauth2_scheme)],
    room_name: Annotated[str, Query(min_length=1, max_length=20)],
):
    user = await get_current_user(token)

    if user.role not in ["Mod", "Admin"]:
        raise HTTPException(
            status_code=400, detail="You do not have permission.")

    newRoom = addRoom(user.role, room_name)

    if not newRoom:
        raise HTTPException(status_code=400, detail="Error adding new room.")

    return newRoom
