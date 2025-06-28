import psycopg


def init_db():
    # create the DB
    with psycopg.connect("dbname=postgres user=postgres", autocommit=True) as conn:
        conn.execute("DROP DATABASE IF EXISTS chatapp")
        conn.execute('DROP ROLE IF EXISTS "Admin"')
        conn.execute('DROP ROLE IF EXISTS "Mod"')
        conn.execute('DROP ROLE IF EXISTS "User";')
        conn.execute("CREATE DATABASE chatapp")

    # metadata of DB
    with psycopg.connect("dbname=chatapp user=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE users(
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(20) NOT NULL,
                    hashed_password TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'User'
                );

                CREATE TABLE rooms(
                    room_id SERIAL PRIMARY KEY,
                    room_name VARCHAR(20) UNIQUE NOT NULL
                );

                CREATE TABLE chats(
                    chat_id SERIAL PRIMARY KEY,
                    room_id INT REFERENCES rooms(room_id),
                    user_id INT REFERENCES users(user_id),
                    message VARCHAR(200) NOT NULL,
                    time TIMESTAMP NOT NULL DEFAULT NOW()
                );

                CREATE ROLE "User";
                GRANT SELECT, INSERT ON chats TO "User";
                GRANT SELECT ON rooms TO "User";
                GRANT USAGE, SELECT, UPDATE ON SEQUENCE chats_chat_id_seq TO "User";

                CREATE ROLE "Mod" INHERIT;
                GRANT "User" TO "Mod";
                GRANT DELETE ON chats TO "Mod";
                GRANT INSERT ON rooms TO "Mod";
                GRANT USAGE, SELECT, UPDATE ON SEQUENCE rooms_room_id_seq TO "Mod";

                CREATE ROLE "Admin" INHERIT;
                GRANT "Mod" TO "Admin";
                GRANT INSERT ON users TO "Admin";
                GRANT SELECT, UPDATE ON users TO "Admin";
                GRANT USAGE, SELECT, UPDATE ON SEQUENCE users_user_id_seq TO "Admin";
            """)


if __name__ == "__main__":
    init_db()
