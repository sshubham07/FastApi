from ..main import app
from ..router.todos import get_current_user,get_db
from starlette import status
from ..models import Todos
from .utils import *

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread":False},
#     poolclass=StaticPool
# )

# TESTINGSESSIONLOCAL = sessionmaker(autocommit = False,autoflush=False,bind=engine)
# Base.metadata.create_all(bind=engine)

# def override_get_db():
#     db = TESTINGSESSIONLOCAL()
#     try:
#         yield db
#     finally:
#         db.close()

# def override_get_current_user():
#     return {'username':'mohan','id':1,'user_role':'admin'}

app.dependency_overrides[get_db]= override_get_db
app.dependency_overrides[get_current_user]= override_get_current_user

# client = TestClient(app)

# @pytest.fixture
# def test_todo():
#     todo = Todos(
#         title = "Learn the code",
#         description = "Need to learn everyday",
#         priority = 2,
#         complete = False,
#         owner_id = 1
#     )
#     db = TESTINGSESSIONLOCAL()
#     db.add(todo)
#     db.commit()
#     yield todo
#     with engine.connect() as connection:
#         connection.execute(text("Delete from todos;"))
#         connection.commit()

def test_all_authenticated(test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    assert response.json() == [{'priority': 2, 'id': 1, 'owner_id': 1, 'complete': False, 'title': 'Learn the code', 'description': 'Need to learn everyday'}]

def test_one_authenticated(test_todo):
    response = client.get('/todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    assert response.json() == {'priority': 2, 'id': 1, 'owner_id': 1, 'complete': False, 'title': 'Learn the code', 'description': 'Need to learn everyday'}

def test_one_not_found(test_todo):
    response = client.get('/todos/todo/99')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    print(response.json())
    assert response.json() == {'detail' :'This todo is not present in the database'}

def test_create_todo(test_todo):
    request_data = {
        "title" : "Learn to ride bike",
        "description" : "Need to learn daily",
        "priority" : 1,
        "complete" : False,
        "owner_id" : 1
    }
    response = client.post('/todos/todo',json = request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db = TESTINGSESSIONLOCAL()
    model = db.query(Todos).filter(Todos.id ==2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority') 
    assert model.owner_id == request_data.get('owner_id')

def test_update_todo(test_todo):
    request_data = {
        "title" : "CHange the title",
        "description" : "Need to learn daily",
        "priority" : 1,
        "complete" : False,
        "owner_id" : 1
    }
    response = client.put('/todos/todo/1',json = request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TESTINGSESSIONLOCAL()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority') 
    assert model.owner_id == request_data.get('owner_id')

def test_update_todo_not_found(test_todo):
    request_data = {
        "title" : "CHange the title",
        "description" : "Need to learn daily",
        "priority" : 1,
        "complete" : False,
        "owner_id" : 1
    }
    response = client.put('/todos/todo/999',json = request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'TODO id not found'}

def test_delete_todo(test_todo):
    request = client.delete('/todos/todo/1')
    assert request.status_code == status.HTTP_204_NO_CONTENT
    db = TESTINGSESSIONLOCAL()
    model = db.query(Todos).filter(Todos.id ==1).first()
    assert model is None

def test_delete_todo_notfound():
    request = client.delete('/todos/todo/999')
    assert request.status_code == status.HTTP_404_NOT_FOUND
    assert request.json() == {'detail':'ToDO id not found'}
