import psycopg
import psycopg.sql as sql
from psycopg.rows import class_row

from .models import User, Chat, Room


# ------------------Modifying rooms and messages-------------------#


def createMsg(caller_role, room_id, user_id, msg):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(Chat)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute(
                    """
                    INSERT INTO chats (room_id, user_id, message)
                    VALUES (%s, %s, %s)
                    RETURNING *;
                    """,
                    (room_id, user_id, msg),
                )
                inserted = cur.fetchone()
                conn.commit()
                return inserted
            except Exception as e:
                conn.rollback()
                print("Error in createMsg:", e)
                return None


def removeMsg(caller_role, chat_id):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(Chat)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute(
                    """
                    DELETE FROM chats
                    WHERE chat_id = %s
                    RETURNING *;
                    """,
                    (chat_id,),
                )
                deleted = cur.fetchone()
                conn.commit()
                return deleted
            except Exception as e:
                conn.rollback()
                print("Error in removeMsg:", e)
                return None


def addRoom(caller_role, room_name):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(Room)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute(
                    """
                    INSERT INTO rooms (room_name)
                    VALUES (%s)
                    RETURNING *;
                    """,
                    (room_name,),
                )
                inserted = cur.fetchone()
                conn.commit()
                return inserted
            except Exception as e:
                conn.rollback()
                print("Error in addRoom:", e)
                return None


# ------------------Modifying users and roles-------------------#


def addUser(caller_role, user_name, hash_pass, role="User"):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(User)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute(
                    """
                    INSERT INTO users (username, hashed_password, role)
                    VALUES (%s, %s, %s)
                    RETURNING *;
                    """,
                    (user_name, hash_pass, role),
                )
                inserted = cur.fetchone()
                conn.commit()
                return inserted
            except Exception as e:
                conn.rollback()
                print("Error in addUser:", e)
                return None


def changeRole(caller_role, user_id, newRole):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(User)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute(
                    """
                    UPDATE users
                    SET role = %s
                    WHERE user_id = %s
                    RETURNING *;
                    """,
                    (newRole, user_id),
                )
                updated = cur.fetchone()
                conn.commit()
                return updated
            except Exception as e:
                conn.rollback()
                print("Error in changeRole:", e)
                return None


# ------------------------select statements----------------------#


def findRoomChats(caller_role, room_id):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(Chat)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute(
                    """
                    SELECT *
                    FROM chats
                    WHERE room_id = %s;
                    """,
                    (room_id,),
                )
                chats = cur.fetchall()
                return chats
            except Exception as e:
                print("Error in findRoomChats:", e)
                return None


def findUser(caller_role, user_id):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(User)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute(
                    """
                    SELECT *
                    FROM users
                    WHERE user_id = %s;
                    """,
                    (user_id,),
                )
                user = cur.fetchone()
                return user
            except Exception as e:
                print("Error in findUser:", e)
                return None


def findUserWithUsername(caller_role, username):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(User)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute(
                    """
                    SELECT *
                    FROM users
                    WHERE username = %s;
                    """,
                    (username,),
                )
                user = cur.fetchone()
                return user
            except Exception as e:
                print("Error in findUser:", e)
                return None


def showRooms(caller_role):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(Room)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute("SELECT * FROM rooms;")
                rooms = cur.fetchall()
                return rooms
            except Exception as e:
                print("Error in showRooms:", e)
                return None


def findRoom(caller_role, room_id):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(Room)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute("SELECT * FROM rooms WHERE room_id = %s;", (room_id,))
                room = cur.fetchone()
                return room
            except Exception as e:
                print("Error in find room:", e)
                return None


def findChat(caller_role, chat_id):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(Chat)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute(
                    """
                    SELECT *
                    FROM chats
                    WHERE chat_id = %s;
                    """,
                    (chat_id,),
                )
                chat = cur.fetchone()
                return chat
            except Exception as e:
                print("Error in find chat:", e)
                return None


def findUsers(caller_role):
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor(row_factory=class_row(User)) as cur:
            try:
                cur.execute(sql.SQL("SET ROLE {}").format(
                    sql.Identifier(caller_role)))
                cur.execute(
                    """
                    SELECT *
                    FROM users
                    """,
                )
                users = cur.fetchall()
                return users
            except Exception as e:
                print("Error in find users:", e)
                return None


# ------------------------testing----------------------#


def insertTestData():
    from .utils.auth import get_password_hash
    data = {}

    users = ["johndoe", "jojo", "justin", "gabe", "wilson"]
    users_in_db = []
    password = get_password_hash("secret")
    for user in users:
        users_in_db.append(addUser("Admin", user, password))

    users_in_db.append(addUser("Admin", "admin", password, "Admin"))
    users_in_db.append(addUser("Admin", "mod", password, "Mod"))
    users_in_db.append(addUser("Admin", "user", password, "User"))

    data["users"] = users_in_db

    rooms = ["cop4521 room", "cop4530 room", "javascript hate club"]
    rooms_in_db = []
    chats_in_db = []
    for room in rooms:
        rooms_in_db.append(addRoom("Admin", room))
        for user in users_in_db:
            chats_in_db.append(
                createMsg(
                    user.role,
                    rooms_in_db[-1].room_id,
                    user.user_id,
                    "hello my name is " + user.username,
                )
            )

    data["rooms"] = rooms_in_db
    data["chats"] = chats_in_db

    return data


if __name__ == "__main__":
    from .init_db import init_db

    init_db()
    data = insertTestData()

    assert showRooms("User") == data["rooms"], "error 1 in show rooms"
    assert showRooms("Mod") == data["rooms"], "error 2 in show rooms"
    assert showRooms("Admin") == data["rooms"], "error 3 in show rooms"

    print("==================show rooms works correctly==================")

    for user in data["users"]:
        assert findUser("Admin", user.user_id) == user, "error in find user"
        assert findUser("Mod", user.user_id) is None, "error in find user"
        assert findUser("User", user.user_id) is None, "error in find user"

    print("==================find user works correctly==================")

    for room in data["rooms"]:
        room_chats = filter(lambda chat: chat.room_id == room.room_id, data["chats"])
        room_chats = list(room_chats)
        assert room_chats == findRoomChats("Admin", room.room_id), "error in find room chats"
        assert room_chats == findRoomChats("Mod", room.room_id), "error in find room chats"
        assert room_chats == findRoomChats("User", room.room_id), "error in find room chats"

        assert room == findRoom("Admin", room.room_id), "error in find room"
        assert room == findRoom("Mod", room.room_id), "error in find room"
        assert room == findRoom("User", room.room_id), "error in find room"

    print("==================find room, room chats works correctly==================")

    for chat in data["chats"]:
        assert chat == findChat("Admin", chat.chat_id), "error in find chat"
        assert chat == findChat("Mod", chat.chat_id), "error in find chat"
        assert chat == findChat("User", chat.chat_id), "error in find chat"

    print("==================find chat works correctly==================")

    assert findUsers("Admin") == data["users"], "error in find users"
    assert findUsers("Mod") is None, "error in find users"
    assert findUsers("User") is None, "error in find users"

    print("==================find users works correcly==================")

    assert data["chats"][0] == removeMsg("Admin", data["chats"][0].chat_id), "error in delete message"
    assert data["chats"][1] == removeMsg("Mod", data["chats"][1].chat_id), "error in delete message"
    assert removeMsg("User", data["chats"][2].chat_id) is None, "error in delete message"

    assert data["chats"][0] not in findRoomChats("User", data["chats"][0].room_id), "error in delete message"
    assert data["chats"][1] not in findRoomChats("User", data["chats"][1].room_id), "error in delete message"

    print("==================deleting a message works correctly==================")

    updatedUser = data["users"][0]
    updatedUser.role = "Mod"
    assert changeRole("Admin", updatedUser.user_id, "Mod") == updatedUser
    assert changeRole("Mod", updatedUser.user_id, "Mod") is None
    assert changeRole("User", updatedUser.user_id, "Mod") is None

    assert findUser("Admin", updatedUser.user_id) == updatedUser

    print("==================change role works correcly==================")
