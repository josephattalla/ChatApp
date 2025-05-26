from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # keep list of connections
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # wait & accept connection, add to active connections
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        # on disconnection remove from active connections
        self.active_connections.remove(websocket)

    async def send_message(self, message: dict, websocket: WebSocket):
        # send message over socket
        await websocket.send_json(message)

    async def broadcast(self, message: dict):
        # send message over all connections
        for connection in self.active_connections:
            await connection.send_json(message)
