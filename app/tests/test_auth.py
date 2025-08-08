import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.deps import get_db
from app.main import app
from app.models.user import User
from app.auth import get_password_hash

# -----------------
# Create in-memory DB
# -----------------

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create tables before any test
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Fixture: mock user
@pytest.fixture
def mock_user():
    db = TestingSessionLocal()
    user = User(
        username="mockuser",
        hashed_password=get_password_hash("mockpass"),
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return {"username": "mockuser", "password": "mockpass"}

# -----------------
# Tests
# -----------------
client = TestClient(app)

def test_login_with_mock_user(mock_user):
    # Login
    r = client.post("/token", data={
        "username": mock_user["username"],
        "password": mock_user["password"]
    })
    assert r.status_code == 200
    token_data = r.json()
    assert "access_token" in token_data

def test_menu_access():
    r = client.get("/menu")
    assert r.status_code == 200
    menu = r.json()
    assert isinstance(menu, list)
    assert len(menu) > 0
