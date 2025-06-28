from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from ..utils.auth import get_current_user, oauth2_scheme
from ..db_functions import changeRole, findUsers

router = APIRouter()


@router.put("/role")
async def changeUserRole(
    token: Annotated[str, Depends(oauth2_scheme)], user_id: int, new_role: str
):
    user = await get_current_user(token)

    if user.role != "Admin":
        raise HTTPException(
            status_code=400, detail="You do not have permissions.")

    if new_role not in ["Mod", "User", "Admin"]:
        raise HTTPException(
            status_code=400, detail="Invalid role choose from: User, Mod, Admin"
        )

    updatedUser = changeRole(user.role, user_id, new_role)

    if not updatedUser:
        raise HTTPException(
            status_code=400, detail="Error changing user's role.")

    del updatedUser.hashed_password
    return updatedUser


@router.get("/users")
async def getAllUsers(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await get_current_user(token)

    if user.role != "Admin":
        raise HTTPException(
            status_code=400, detail="You do not have permissions.")

    users = findUsers(user.role)

    if not users:
        raise HTTPException(status_code=400, detail="Error retrieving users.")

    for user in users:
        del user.hashed_password

    return {"users": users}
