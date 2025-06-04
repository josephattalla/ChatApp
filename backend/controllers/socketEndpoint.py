from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..utils.ConnectionManager import ConnectionManager
from ..models.chats import Chats

router = APIRouter()
manager = ConnectionManager()

chats = Chats()
chats.insertTestData()


# 1. send messages on connection
# 2. receive messages
# 3. update database with message
# 4. broadcast new message
@router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    # connect to clients ws & send chats
    await manager.connect(websocket)
    # await manager.broadcast(f"{client_id} disconnected")
    messages = chats.getChats()
    if messages:
        # messages = json.dumps({"chats": [[m[0], m[1]] for m in messages]})
        await websocket.send_json({"chats": [[m[0], m[1]] for m in messages]})
        print("sent:", messages)
    try:
        while True:
            # wait for a message from connected client & broadcast it
            data = await websocket.receive_text()
            print("received:", data)
            chats.addChat(client_id, data)
            print("new db:", chats.getChats())
            await manager.broadcast({"chats": [[client_id, data]]})
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        # await manager.broadcast(f"{client_id} disconnected")
