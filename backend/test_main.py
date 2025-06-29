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
    room_id = initialData["rooms"][0].room_id

    # test gets all rooms for a authenticated user
    response = client.get("api/rooms", headers={"Authorization": "bearer " + tokens["user"]})
    assert response.status_code == 200
    assert response.json() == {"rooms": [room.model_dump() for room in initialData["rooms"]]}

    # test failing without a token
    response = client.get("/api/rooms")
    assert response.status_code == 401

    # test a valid message to a valid room
    data = {"message": "Hello world!"}
    response = client.post(
        f"/api/rooms/{room_id}",
        json=data,
        headers={"Authorization": "bearer " + tokens["user"]}
    )
    assert response.status_code == 201
    assert response.json()["message"] == data["message"]

    # declaring the message id to test the deletions later in function
    message_id = response.json()["chat_id"]

    # test an invalid/empty message
    data = {"message": ""}
    response = client.post(
        f"/api/rooms/{room_id}",
        json=data,
        headers={"Authorization": "bearer " + tokens["user"]}
    )
    assert response.status_code == 422

    # test invalid room id
    data = {"message": "Test"}
    response = client.post(
        "/api/rooms/9999",
        json=data,
        headers={"Authorization": "bearer " + tokens["user"]}
    )
    assert response.status_code == 400

    # test post with no token
    response = client.post(f"/api/rooms/{room_id}", json={"message": "Test"})
    assert response.status_code == 401

    # test valid deletion
    response = client.delete(
        f"/api/rooms/{room_id}/{message_id}",
        headers={"Authorization": "bearer " + tokens["user"]}
    )
    assert response.status_code == 200
    assert response.json()["chat_id"] == message_id

    # test invalid message id
    response = client.delete(
        f"/api/rooms/{room_id}/99999",
        headers={"Authorization": "bearer " + tokens["user"]}
    )
    assert response.status_code == 400

    # test delete with no token
    response = client.delete(f"/api/rooms/{room_id}/{message_id}")
    assert response.status_code == 401

    # TODO: finish testing rooms

def test_login():
    # test successful login
    data = {
        "username": initialData["users"][0].username,
        "password": "secret"
    }
    response = client.post("/api/login", data=data)
    assert response.status_code == 200
    json_resp = response.json()
    assert "access_token" in json_resp
    assert json_resp["token_type"] == "bearer"
    assert json_resp["username"] == data["username"]
    assert "user_id" in json_resp

    # test for wrong password
    data = {
        "username": initialData["users"][0].username,
        "password": "wrongpassword"
    }
    response = client.post("/api/login", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

    # test login with missing password
    response = client.post("/api/login", data={"username": data["username"]})
    assert response.status_code == 422

    # TODO tests for Admin endpoints
    # TODO tests for Mod endpoints
    # TODO tests for Websokcet endpoints
    # TODO tests for session endpoints

# TODO: For each endpoint test:
#   - invalid inputs (for posts or URLS w/queries)
#   - invalid authentications via admin, mod, user tokens
#       (for protected endpoints)
#   - correct input data with expected status code + returned data
