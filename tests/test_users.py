from app import schemas
from jose import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Welcome to a new fastapi projects"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "sandman@gmail.com", "password": "asd123"}
    )
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "sandman@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": "sandman@gmail.com", "password": "asd123"}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")

    assert user_id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
