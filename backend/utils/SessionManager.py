import uuid


class SessionManager:
    def __init__(self):
        # {user_id: session_id}
        self.sessions = dict()

    def getSession(self, user_id: int):
        # TODO: Check if user_id is in DB
        if user_id in self.sessions:
            return self.sessions[user_id]
        newSessionId = str(uuid.uuid4())
        self.sessions[user_id] = newSessionId
        return newSessionId

    def invalidSession(self, user_id: int, session_id: str):
        print("*******************", self.sessions)
        return user_id not in self.sessions or self.sessions[user_id] != session_id

    def deleteSession(self, user_id: int):
        if user_id in self.sessions:
            del self.sessions[user_id]


sessionManager = SessionManager()
