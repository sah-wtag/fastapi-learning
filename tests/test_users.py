from fastapi.testclient import TestClient
from app import schemas
from app.database import get_db, Base
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://welldev:abir1234@localhost/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.json().get("message") == "Welcome to a new fastapi projects"
    assert res.status_code == 200


def test_create_user():
    res = client.post(
        "/users/", json={"email": "sandman@gmail.com", "password": "asd123"}
    )
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "sandman@gmail.com"
    assert res.status_code == 201
