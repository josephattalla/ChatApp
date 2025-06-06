from fastapi import FastAPI
from pydantic import BaseModel

class Chat(BaseModel):
    chat_id: int
    room_id: int
    user_id: int
    message: str
    time: str

class Rooms(BaseModel):
    room_id: int
    room_name: str

class Users(BaseModel):
    user_id: int
    username: str
    hash_pass: str

def createChatTable(self):
        conn, cursor = self.connect()
        cursor.execute("DROP TABLE IF EXISTS chats")
        cursor.execute("""
            CREATE TABLE chats (
                chat_id INT,
                room_id INT,
                user_id INT,
                message TEXT,
                time TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)
        self.disconnect(conn, cursor)

def ChatIdSeq(self):
    ("""
    CREATE SEQUENCE chat_chat_id
    START 1
    INCREMENT 1
    MINVALUE 1
    OWNED BY chats.chat_id;
    """)

def createRoomTable(self):
    ("""
    CREATE TABLE rooms (
        room_id INT
        room_name TEXT
    ); 
    """)

def RoomIDSeq(self):
    ("""
    CREATE SEQUENCE rooms_room_id
    START 0
    INCREMENT 1
    MINVALUE 1
    OWNED BY rooms.room_id;
    """)

def addRoom():
    ("""
    INSERT INTO rooms VALUES (nextval('room_id'), {room.name}
    ); 
    """)


#users table already exists in db

#
def CreateUsersTable(self):
    ("""
    CREATE TABLE users (
        user_id INT,
        username VARCHAR(120) NOT NULL,
        hashed_password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT = 'user'
        );
    """)

def userIdSeq(self):
    ("""
    CREATE SEQUENCE
    START 1
    INCREMENT 1
    MINVALUE 1
    OWNED BY users.user_id;
    """)

def AddUser(self):
    ("""
    INSERT INTO Users VALUES (next('user_id'), {username}, {hash_pass}, {role}
    );
    """)

def makeMod(self):
    ("""
    GRANT Mod TO {user_id};
    """)

def removeMod(self):
    ("""
    REVOKE Mod FROM {user_id};
    """)


#mod grants / can delete msg and rooms / cannot add mods
def grantModPerms(self):
    ("""
    GRANT SELECT | DELETE ON chats TO Mod;


    GRANT ALTER 


    """)

def grantAdmin(self):

def createUser(self):
    ("""
    CREATE USER {username};
    """)

def createRoles(self):
    ("""
    CREATE ROLE Mod; """)
