# from fastapi import FastAPI
# from pydantic import BaseModel

# class Chat(BaseModel):
#     chat_id: int
#     room_id: int
#     user_id: int
#     message: str
#     time: str

# class Rooms(BaseModel):
#     room_id: int
#     room_name: str

# class Users(BaseModel):
#     user_id: int
#     username: str
#     hash_pass: str

# app = FastAPI()

import pyscopg

from psycopg import sql

with psycopg.connect("dbname = chatApp user=postgres") as conn:
    with conn.cursor() as cursor:

        cursor.execute("""
        CREATE TABLE users (
            user_id INT PRIMARY KEY,
            username VARCHAR(120) NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
            );
        CREATE SEQUENCE users_user_id
            START 1
            INCREMENT 1
            MINVALUE 1
            OWNED BY users.user_id;
        CREATE TABLE rooms (
            room_id INT PRIMARY KEY,
            room_name VARCHAR(20) UNIQUE NOT NULL
            ); 
        CREATE SEQUENCE rooms_room_id
            START 1
            INCREMENT 1
            MINVALUE 1
            OWNED BY rooms.room_id;
        CREATE TABLE room_members (
            role TEXT NOT NULL,
            user_id INT REFERENCES users(user_id),
            room_id INT REFERENCES rooms(room_id)
            );
        CREATE TABLE chats (
            chat_id INT PRIMARY KEY,
            room_id INT REFERENCES rooms(room_id),
            user_id INT REFERENCES users(user_id),
            message VARCHAR(200) NOT NULL,
            time TIMESTAMP NOT NULL DEFAULT NOW()
            );
        CREATE SEQUENCE chat_chat_id
            START 1
            INCREMENT 1
            MINVALUE 1
            OWNED BY chats.chat_id;
        """)

#--------------------------------------------#

#------------------Adding rooms and messages-------------------#

#variable
def createMsg():
    makeMsg = """
    INSERT INTO chats (chat_id, room_id, user_id, message, timestamp)
    VALUES (next('chat_id'), %s, %s, %s, %s);
    """
    msgData = (room_id, user_id, msg, time)
    cursor.execute(makeMsg, msgData)

#variable
def addRoom():
    addroom = """
    INSERT INTO rooms (room_id, room_name) 
    VALUES (nextval('room_id), %s);
    """
    roomName = (room_name)
    cursor.execute(addroom, roomName)

#------------------Modifying users and roles-------------------#

#variable
def AddUser():
    add_user = """
    INSERT INTO Users (user_id, username, hashed_password, role) 
    VALUES (next('user_id'),%s, %s, %s)
    """
    userData = (user_name, hash_pass, role)
    cursor.execute(add_user, userData)

#variable / users are found in pg_user table
def createUser():
    makeUser = """
    CREATE USER %s;
    """
    userName = (user_name)
    cursor.execute(makeUser, userName)

#user roles are found in pg_roles
def createRoles():

    cursor.execute("""
        CREATE ROLE Mod;
    """)

#mod grants / can delete msg and rooms / cannot add mods
def grantModPerms():

    cursor.execute("""
    GRANT SELECT | DELETE ON chats TO Mod;
    """)
    cursor.execute("""
    GRANT ALTER | CASCADE ON rooms TO Mod;
    """)

#variable
def makeMod():
    grantMod = """
    GRANT Mod TO %s;
    """
    modName = (mod_name)
    cursor.execute(grantMod, modName)

#variable
def removeMod():
    revokeMod = """
    REVOKE Mod FROM %s;
    """
    modName = (mod_name)
    cursor.execute(revokeMod, modName)

#close connections
cursor.close()
conn.close()