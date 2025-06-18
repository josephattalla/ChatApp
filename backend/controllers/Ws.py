from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from ..utils.RoomsManager import roomsManager
from ..utils.SessionManager import sessionManager

router = APIRouter()

# TODO: implement as: /roomid?sessionid=...
# fix 403 forbidden problem


@router.websocket("/{room_id}")
async def ws(room_id: int, user_id: int, session_id: str, websocket: WebSocket):
    # TODO: change token to a session id & check its
    # validity and mapping to which user
    # TODO: add database lookup to check validity of room id

    if sessionManager.invalidSession(user_id, session_id):
        raise HTTPException(status_code=401, detail="Invalid creditation")

    sessionManager.deleteSession(user_id)

    await roomsManager.connect(room_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print("received:", data)
    except WebSocketDisconnect:
        await roomsManager.disconnect(room_id, websocket)
