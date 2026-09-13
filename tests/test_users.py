from app import schemas
from .database import client, session


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


def test_login_user(client):
    # client.post(
    #     "/users/", json={"email": "sandman@gmail.com", "password": "asd123"}
    # )
    res = client.post(
        "/login", data={"username": "sandman@gmail.com", "password": "asd123"}
    )
    print(res.json())
    assert res.status_code == 200
