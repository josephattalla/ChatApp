import pyscopg
from psycopg import sql

#------------------Modifying rooms and messages-------------------#

def createMsg(room_id, user_id, msg, time):  
    with psycopg.connect("dbname = chatApp user=postgres") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                INSERT INTO chats (chat_id, room_id, user_id, message, timestamp)
                VALUES (next('chat_id'), %s, %s, %s, %s);
                """, (room_id, user_id, msg, time))
                cur.commit()
            except:
                return False
    
def removeMsg(chat_id):
    with psycopg.connect("dbname = chatApp user=postgres") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                SET ROLE Mod
                DELETE FROM chats
                WHERE chat_id = %s;
                """, (chat_id))
                cur.commit()
            except:
                return False

def addRoom(room_name):
    with psycopg.connect("dbname = chatApp user=postgres") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                SET ROLE Mod
                INSERT INTO rooms (room_id, room_name) 
                VALUES (nextval('room_id), %s);
                """, (room_name))
                conn.commit()
            except:
                return False

#------------------Modifying users and roles-------------------#

def AddUser(user_name, hash_pass, role):
    with psycopg.connect("dbname = chatApp user=postgres") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                SET ROLE Mod
                INSERT INTO Users (user_id, username, hashed_password, role) 
                VALUES (next('user_id'),%s, %s, %s);
                """, (user_name, hash_pass, role))
                conn.commit()
            except:
                return False


def changeRole(userName, newRole):
    with psycopg.connect("dbname = chatApp user=postgres") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                SET ROLE Mod
                UPDATE users
                SET role = %s
                WHERE username = %s;
                """, (userName, newRole))
                conn.commit()
            except:
                return False

#------------------------select statements----------------------#

#shows chats by room_id
def findRoomChats(room_id):
    with psycopg.connect("dbname = chatApp user=postgres") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                SELECT chats.message 
                FROM chats 
                WHERE room_id = %s;
                """, (room_id))
                conn.commit()
            except:
                return False

#finds users by their username
def findUser(userName):
    with psycopg.connect("dbname = chatApp user=postgres") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                SELECT * 
                FROM users 
                WHERE username = %s;""", (userName))
                conn.commit()
            except:
                return False

#shows available rooms
def showRooms():
    with psycopg.connect("dbname = chatApp user=postgres") as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                SELECT * 
                FROM rooms;""")
            except:
                return False

    conn.commit()