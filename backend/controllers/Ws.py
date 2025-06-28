from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from ..utils.RoomsManager import roomsManager
from ..utils.SessionManager import sessionManager
from ..db_functions import findRoom, findUser, findRoomChats

router = APIRouter()


@router.websocket("/{room_id}")
async def ws(room_id: int, user_id: int, session_id: str, websocket: WebSocket):
    # check validity of room id & user id
    user = findUser("Admin", user_id)
    if not user:
        raise HTTPException(status_code=400)
    room = findRoom(user.role, room_id)
    if not room:
        raise HTTPException(status_code=400)

    if sessionManager.invalidSession(user_id, session_id):
        raise HTTPException(status_code=401, detail="Invalid creditation")

    sessionManager.deleteSession(user_id)

    await roomsManager.connect(room_id, websocket)

    try:
        # send room chats to newly connected user
        roomChats = findRoomChats(user.role, room.room_id)
        if roomChats:
            messages = []
            for chat in roomChats:
                chatUser = findUser("Admin", chat.user_id)
                currChat = chat.model_dump()
                currChat["time"] = str(currChat["time"])
                messages.append(
                    {
                        "chat": currChat,
                        "username": chatUser.username if chatUser else "",
                    }
                )
            message = {"type": "room messages", "messages": messages}
            await websocket.send_json(message)

        while True:
            data = await websocket.receive_text()
            print("received:", data)
    except WebSocketDisconnect:
        await roomsManager.disconnect(room_id, websocket)
