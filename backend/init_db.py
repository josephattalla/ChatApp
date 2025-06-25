import pyscopg

from psycopg import sql

with psycopg.connect("dbname = chatApp user=postgres") as conn:
    with conn.cursor() as cur:

        cur.execute("""
        CREATE TABLE users (
            user_id INT PRIMARY KEY,
            username VARCHAR(120) NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'User'
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
        CREATE ROLE Mod;
        GRANT SELECT | DELETE ON chats TO Mod;
        GRANT SELECT | UPDATE | ALTER ON users TO Mod;
        GRANT SELECT | ALTER | CASCADE ON rooms TO Mod;
        """)

cur.close()
conn.close()