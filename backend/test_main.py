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
        headers={"Authorization" :f"bearer {tokens['user']}"}
    )
    assert response.status_code == 201
    assert response.json()["message"] == data["message"]

    # declaring the message id to test the deletions later in function
    message_id = response.json()["chat_id"]

    # test message that is too long
    temp_long_message = "a" * 201
    response = client.post(
        f"/api/rooms/{room_id}",
        json={"message": temp_long_message},
        headers={"Authorization" :f"bearer {tokens['user']}"}
        )
    assert response.status_code in (400, 422)

    # test an invalid/empty message
    data = {"message": ""}
    response = client.post(
        f"/api/rooms/{room_id}",
        json=data,
        headers={"Authorization" :f"bearer {tokens['user']}"}
    )
    assert response.status_code == 422

    # test invalid room id
    data = {"message": "Test"}
    response = client.post(
        "/api/rooms/9999",
        json=data,
        headers={"Authorization" :f"bearer {tokens['user']}"}
    )
    assert response.status_code == 400

    # test post with no token
    response = client.post(f"/api/rooms/{room_id}", json={"message": "Test"})
    assert response.status_code == 401

    # test valid deletion
    response = client.delete(
        f"/api/rooms/{room_id}/{message_id}",
        headers={"Authorization" :f"bearer {tokens['user']}"}
    )
    assert response.status_code == 200
    assert response.json()["chat_id"] == message_id

    # test invalid message id
    response = client.delete(
        f"/api/rooms/{room_id}/99999",
        headers={"Authorization" :f"bearer {tokens['user']}"}
    )
    assert response.status_code == 400

    # test delete with no token
    response = client.delete(f"/api/rooms/{room_id}/{message_id}")
    assert response.status_code == 401



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

    # test login attempt with nonexistent username
    data = {
        "username" : "place",
        "password" : "holder"
    }
    response = client.post("/api/login", data=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

    # test login with empty form request (no data entered)
    response = client.post("/api/login")
    assert response.status_code == 422



def test_admin():
    # test admin changing role successfully
    target_user_id = initialData["users"][1].user_id
    response = client.put(
        "/api/role",
        params={"user_id": target_user_id, "new_role": "Mod"},
        headers={"Authorization" :f"bearer {tokens['admin']}"}
    )
    assert response.status_code == 200
    assert response.json()["role"] == "Mod"

    # test non-admin trying to change roles
    response = client.put(
        "/api/role",
        params={"user_id": target_user_id, "new_role": "Mod"},
        headers={"Authorization" :f"bearer {tokens['user']}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "You do not have permissions"

    # test setting an invalid role
    response = client.put(
        "/api/role",
        params={"user_id": target_user_id, "new_role": "FakeRole"},
        headers={"Authorization" :f"bearer {tokens['admin']}"}
    )
    assert response.status_code == 400
    assert "Invalid role" in response.json()["detail"]

    # test changing role with no token possessed
    response = client.put(
        "/api/role",
        params={"user_id" : target_user_id, "new_role" : "Mod"},
    )
    assert response.status_code == 401

    # test admin successfully getting all users
    response = client.get(
        "/api/users",
        headers={"Authorization" : f"bearer {tokens['admin']}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json()["users"], list)
    assert len(response.json()["users"]) >= 1
    assert "hashed_password" not in response.text

    # test non-admin trying to get all users
    response = client.put(
        "/api/role",
        headers={"Authorization" : f"bearer {tokens['mod']}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "You do not have permissions."

    # test getting all users with no token
    response = client.get("/api/users")
    assert response.status_code == 401

    # TODO tests for Mod endpoints
    # TODO tests for Websokcet endpoints
    # TODO tests for session endpoints

# TODO: For each endpoint test:
#   - invalid inputs (for posts or URLS w/queries)
#   - invalid authentications via admin, mod, user tokens
#       (for protected endpoints)
#   - correct input data with expected status code + returned data
