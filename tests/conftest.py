from fastapi.testclient import TestClient
import pytest
from app import models
from app.database import get_db, Base
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = "postgresql://welldev:abir1234@localhost/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_user(client):
    user_data = {"email": "sandman@gmail.com", "password": "asd123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    return new_user


@pytest.fixture()
def session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "First post",
            "content": " First content",
            "owner_id": test_user["id"],
        },
        {
            "title": "2nd post",
            "content": " 2nd content",
            "owner_id": test_user["id"],
        },
        {
            "title": "3rd post",
            "content": " 3rd content",
            "owner_id": test_user["id"],
        },
    ]

    posts = [models.Post(**post) for post in posts_data]

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
