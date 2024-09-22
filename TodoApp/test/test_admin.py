from .utils import *
from ..router.admin import get_db, get_current_user
from starlette import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get('/admin/todo')
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    assert response.json() == [{'title' : "Learn the code",'description' : 'Need to learn everyday','priority' : 2,'complete' : False, 'owner_id' : 1,'id':1}]


def test_admin_delete_todo(test_todo):
    response = client.delete('/admin/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TESTINGSESSIONLOCAL()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_admin_delete_admin_not_found(test_todo):
    response = client.delete('/admin/todo/99')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Todo id Not found'}
