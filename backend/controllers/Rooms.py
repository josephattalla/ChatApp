from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from ..db_functions import showRooms, createMsg, findRoom, removeMsg
from ..utils.auth import get_current_user, oauth2_scheme
from ..utils.RoomsManager import roomsManager
from pydantic import BaseModel, Field


class MessageBody(BaseModel):
    message: str = Field(..., min_length=1, max_length=200)


router = APIRouter()


# GET (return all rooms with their names and IDs)
@router.get("/rooms")
async def getRooms(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await get_current_user(token)

    rooms = showRooms(user.role)
    return {"rooms": rooms}


# POST (post message to corresponding room ID)
@router.post("/rooms/{room_id}", status_code=201)
async def postMessage(
    room_id: int, token: Annotated[str, Depends(oauth2_scheme)], body: MessageBody
):
    user = await get_current_user(token)

    message = body.message
    if len(message) > 200 or len(message) < 1:
        raise HTTPException(status_code=400)

    room = findRoom(user.role, room_id)
    if not room:
        raise HTTPException(status_code=400)

    chat = createMsg(user.role, room.room_id, user.user_id, message)
    if not chat:
        raise HTTPException(status_code=400)

    chat = chat.model_dump()
    chat["time"] = str(chat["time"])
    newMessage = {"type": "new chat", "chat": chat, "username": user.username}
    await roomsManager.broadcastMessage(room.room_id, newMessage)

    return chat


# DELETE (deletes message in corresponding room ID)
@router.delete("/rooms/{room_id}/{message_id}", status_code=200)
async def deleteMessage(
    room_id: int, token: Annotated[str, Depends(oauth2_scheme)], message_id: int
):
    user = await get_current_user(token)

    room = findRoom(user.role, room_id)
    if not room:
        raise HTTPException(status_code=400)

    deletedChat = removeMsg(user.role, message_id)
    if not deletedChat:
        raise HTTPException(status_code=400)

    newMessage = {"type": "deleted message", "chat_id": deletedChat.chat_id}
    await roomsManager.broadcastMessage(room.room_id, newMessage)

    return deletedChat
