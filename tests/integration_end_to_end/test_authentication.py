from flask import session
from tests.integration_end_to_end.utils import client



def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the CS235 Game library!" in response.data

def test_register(client):
    with client:
        response = client.get("/authentication/register")
        assert session.get('username') == None
        assert response.status_code == 200
        assert b"Register" in response.data

        response = client.post("/authentication/register", data={"user_name": "test", "password": "test", "confirm_password": "test"}, follow_redirects=True) # try too short password
        assert b'Password must be at least 6' in response.data
        response = client.post("/authentication/register", data={"user_name": "test", "password": "sixsix", "confirm_passwrd": "sixsix"}, follow_redirects=True) # try too short password no capital password
        assert b'contain at least one uppercase' in response.data
        response = client.post("/authentication/register", data={"user_name": "test", "password": "Sixsix", "confirm_password": "Sixsix"}, follow_redirects=True) # try too short password no digit password
        assert b'and one digit' in response.data
        assert session.get('username') == None
        response = client.post("/authentication/register", data={"user_name": "el", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True) # try too short username
        assert b'must be at least 3 characters long' in response.data # try invalid username/password combination

        response = client.post("/authentication/register", data={"user_name": "test", "password": "Sixsix8", "confirm_password": "Sixsix7"}, follow_redirects=True) # try mismatching passwords

        response = client.post("/authentication/register", data={"user_name": "test", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True) # try valid username/password combination
        assert session.get('username') == 'test'  # check if the user is logged in
        assert b'Welcome to the CS235 Game library!' in response.data # check if the user is redirected to the home page

        response = client.get("/authentication/logout", follow_redirects=True)
        assert session.get('username') == None
        response = client.post("/authentication/register", data={"user_name": "test", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True) # try registering an existing user
        assert b'Username already taken.' in response.data
        assert session.get('username') == None  # check if the user is logged in
        assert response.status_code == 409  # check if the correct status code is returned (conflict)

        response = client.post("/authentication/register", data={"user_name": "test2", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True) # try registering a new user
        assert session.get('username') == 'test2'  # check if the user is logged in

def test_login(client):
    with client:
        response = client.post("/authentication/register", data={"user_name": "test", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True) # register a user
        assert session.get('username') == 'test'  # check if the user is logged in
        response = client.get("/authentication/logout", follow_redirects=True) # log out
        assert session.get('username') == None

        response = client.post("/authentication/login", data={"user_name": "test2", "password": "Sixsix7"}, follow_redirects=True) # try logging in with an ivalid username/password combination
        assert session.get('username') == None
        assert response.status_code == 401

        response = client.post("/authentication/login", data={"user_name": "test", "password": "Sixsix7"}, follow_redirects=True)
        assert session.get('username') == 'test'  # check if the user is logged in
        assert b'Welcome to the CS235 Game library!' in response.data # check if the user is redirected to the home page

def test_logout(client):
    with client:
        response = client.get("/") #  get the index simply so we can get a request context for session
        assert session.get('username') == None  # check if the user is logged in
        response = client.get("/authentication/logout", follow_redirects=True)
        assert response.status_code == 401  # assert that if we are not logged in we cant log out
        assert session.get('username') == None  # check if the user is logged in

        response = client.post("/authentication/register", data={"user_name": "test", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True) # register a user
        assert session.get('username') == 'test'  # check if the user is logged in
        response = client.get("/authentication/logout", follow_redirects=True) # log out
        assert session.get('username') == None
