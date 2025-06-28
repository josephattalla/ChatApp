from fastapi.testclient import TestClient

from .main import app
from .init_db import init_db
from .db_functions import insertTestData
from .utils.auth import create_access_token

client = TestClient(app)


init_db()
initialData = insertTestData()
# NOTE: initalData:
#   - ["users"]: list of inserted users, each a User model from models.py
#       - all plain passwords are "secret"
#   - ["rooms"]: list of inserted rooms, each a Room model from models.py
#   - ["chats"]: list of inserted users, each a Chat model from models.py

# tokens to user to test user, mode, and user access to protected endpoints
tokens = {"admin": "", "mod": "", "user": ""}
for user in tokens.keys():
    tokens[user] = create_access_token(data={"sub": user})


def test_register():
    # test registering w/invalid username
    data = {"username": "a", "password": "password1234"}
    response = client.post("/api/register", json=data)
    assert response.status_code == 422

    # test registering w/invalid password
    data = {"username": "abcdefg", "password": "1234"}
    response = client.post("/api/register", json=data)
    assert response.status_code == 422

    # test registering with in use username
    data = {"username": initialData["users"]
            [0].username, "password": "password1234"}
    response = client.post("/api/register", json=data)
    print(response.text)
    assert response.status_code == 409

    # test successful registration
    data = {"username": "abcdefg", "password": "password1234"}
    response = client.post("/api/register", json=data)
    assert response.status_code == 201
    assert response.json()["username"] == data["username"]


def test_rooms():
    # test gets all rooms for a authenticated user
    response = client.get("api/rooms", headers={"Authorization": "bearer " + tokens["user"]})
    assert response.status_code == 200
    assert response.json() == {"rooms": [room.model_dump() for room in initialData["rooms"]]}

    # TODO: finish testing rooms

# TODO: For each endpoint test:
#   - invalid inputs (for posts or URLS w/queries)
#   - invalid authentications via admin, mod, user tokens
#       (for protected endpoints)
#   - correct input data with expected status code + returned data
