import psycopg2


class Chats:
    def __init__(self):
        self.setupDB("chatapp")
        self.createTable()

    def connect(self):
        conn = psycopg2.connect(user="postgres", password="postgres", dbname="chatapp")
        conn.autocommit = True
        cursor = conn.cursor()
        return conn, cursor

    def disconnect(self, conn, cursor):
        cursor.close()
        conn.close()

    def createTable(self):
        conn, cursor = self.connect()
        cursor.execute("DROP TABLE IF EXISTS chats")
        cursor.execute("""
            CREATE TABLE chats (
                user_id INTEGER,
                message TEXT,
                time TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)
        self.disconnect(conn, cursor)

    def addChat(self, user_id: int, message: str):
        conn, cursor = self.connect()
        cursor.execute(
            "INSERT INTO chats (user_id, message) VALUES (%s, %s)", (user_id, message)
        )
        self.disconnect(conn, cursor)

    def getChats(self):
        conn, cursor = self.connect()
        cursor.execute("SELECT user_id, message FROM chats ORDER BY time ASC")
        data = cursor.fetchall()
        self.disconnect(conn, cursor)
        return data

    def insertTestData(self):
        testData = [
            (1, "test1"),
            (2, "test2"),
            (3, "test3"),
            (4, "test4"),
            (5, "test5"),
        ]
        for user, data in testData:
            self.addChat(user, data)

    def setupDB(self, dbName: str):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {dbName}")
        cursor.execute(f"CREATE DATABASE {dbName}")
        self.disconnect(conn, cursor)


if __name__ == "__main__":
    chats = Chats()
    chats.insertTestData()
    print(chats.getChats())
    chats.addChat(69, "hello!")
    print(chats.getChats())
