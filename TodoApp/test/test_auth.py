from .utils import *
from ..router.auth import get_current_user,get_db,authenticate_user,create_access_token,ALGORITHM,SECRET_KEY
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException
app.dependency_overrides[get_db] = override_get_db
#app.dependency_overrides[get_current_user] =override_get_current_user

def test_authenticate_user(test_user):
    db = TESTINGSESSIONLOCAL()
    authenticated_user = authenticate_user(test_user.username, 'mohan',db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username
    non_existance_user = authenticate_user('wronguser','wrongpassword',db)
    assert non_existance_user == False

def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)
    token = create_access_token(username, user_id, role, expires_delta)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature':False})
    assert decoded.get('sub') ==username
    assert decoded.get('id') ==user_id
    assert decoded.get('role') == role
@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub':'user', 'id':1,'role':'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    decoded = await get_current_user(token)
    assert decoded.get('username') == encode.get('sub')
    assert decoded.get('id') == encode.get('id')
    assert decoded.get('user_role') == encode.get('role')

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'sub':'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not velidate user'



