from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..models import Base, Todos, Users
from fastapi.testclient import TestClient
import pytest
from ..main import app
from ..router.auth import bycrypt_context
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False},
    poolclass=StaticPool
)

TESTINGSESSIONLOCAL = sessionmaker(autocommit = False,autoflush=False,bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TESTINGSESSIONLOCAL()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'mohan','id':1,'user_role':'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn the code",
        description = "Need to learn everyday",
        priority = 2,
        complete = False,
        owner_id = 1
    )
    db = TESTINGSESSIONLOCAL()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("Delete from todos;"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
                username='mohan1',
                phone_number='1111111',
                first_name='mohan',
                last_name='mohan',
                hashed_password=bycrypt_context.hash('mohan'),
                role='admin',
                email='mohan1@gmail.com'
            )
    db = TESTINGSESSIONLOCAL()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("Delete from Users;"))
        connection.commit()

