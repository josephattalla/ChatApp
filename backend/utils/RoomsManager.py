from fastapi import WebSocket


class RoomsManager:
    def __init__(self):
        # {room_id : {WebSocket,...}}
        self.active_connections: dict[int, set[WebSocket]] = {}

    async def connect(self, room_id: int, websocket: WebSocket):
        # wait & accept connection, add to active connections
        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        self.active_connections[room_id].add(websocket)

    async def disconnect(self, room_id: int, websocket: WebSocket):
        # on disconnection remove from active connections
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if len(self.active_connections[room_id]) == 0:
                del self.active_connections[room_id]

    async def broadcastMessage(self, room_id, message: dict):
        if room_id in self.active_connections:
            for ws in self.active_connections[room_id]:
                await ws.send_json(message)


roomsManager = RoomsManager()
