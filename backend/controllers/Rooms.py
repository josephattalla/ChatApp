from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Temp room item
class Room(BaseModel):
    room_id : int
    room_name : str

class RoomList(BaseModel):
    rooms : list[Room]

# Temp data for testing 
testRooms = RoomList(rooms = [Room(room_id = 1, room_name = "First Room"),
         Room(room_id = 2, room_name = "Second Room"),
         Room(room_id = 3, room_name = "Third Room")])

class Message(BaseModel):
    text : str

class MessageID(BaseModel):
    id : int

# GET (return all rooms with their names and IDs)
@router.get("/rooms")
async def getRooms():
    return testRooms

# POST (post message to corresponding room ID)
@router.post("/api/rooms/{roomid}", status_code = 201)
async def postMessage(message : Message):
    return

# DELETE (deletes message in corresponding room ID)
@router.delete("/api/rooms/{roomid}", status_code = 200)
async def deleteMessage(message_id : MessageID):
    return