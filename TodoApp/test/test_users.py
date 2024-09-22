from .utils import *
from ..router.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get('/users/user_info')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'mohan1'

def test_user_change_password(test_user):
    response  = client.put('/users/update_password',json={'password':'mohan','new_password':'mohan1'})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_user(test_user):
    response  = client.put('/users/update_password',json={'password':'mohan1','new_password':'mohan2'})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    print(response.json())
    assert response.json() == {'detail':'Old password did not match'}

def test_detail_phone_number_change_success(test_user):
    response = client.put('/users/update_phonenumber/',json={'new_number':'22222222222'})
    assert response.status_code == status.HTTP_204_NO_CONTENT
