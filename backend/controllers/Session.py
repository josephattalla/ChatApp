from fastapi import APIRouter, Depends
from typing import Annotated

from ..utils.SessionManager import sessionManager
from .Login import oauth2_scheme, get_current_user

router = APIRouter()


@router.post("/session")
async def getSession(token: Annotated[str, Depends(oauth2_scheme)]):
    # verify user, sends 401 unauthorized if not verified
    user = await get_current_user(token)

    newSessionId = sessionManager.getSession(user.user_id)

    return {"session_id": newSessionId}
