from tests.integration_end_to_end.utils import client
from flask import session, request

def test_profile(client):

    with client:
        response = client.get("/profile", follow_redirects=False)
        assert response.status_code == 308 # assert that when we are not logged in we get a redirect

        response = client.get("/profile", follow_redirects=True)
        assert response.status_code == 200 # assert that when we are not logged in we get a 401

        assert request.path == "/authentication/login" # assert that we are redirected to the login page

        response = client.post("/authentication/register", data={"user_name": "test", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True) # register a user
        assert session.get('username') == 'test'  # check if the user is logged in

        response = client.get("/profile", follow_redirects=True)
        assert response.status_code == 200 # assert that when we are logged in we get a 200
        assert request.path == "/profile" # assert that we are sent to the profile page

        response = client.get("/profile/test", follow_redirects=True)
        assert response.status_code == 200 # assert that when we are logged in we get a 200
        assert request.path == "/profile/test" # assert that we are sent to the profile page

def test_other_user_profile(client):
    with client:
        response = client.get('/')
        assert session.get('username') == None

        response = client.get("/profile/eli", follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/authentication/login" # assert that we are redirected to the login page if we aren't logged in

        response = client.post("/authentication/register", data={"user_name": "test", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True) # register a user
        assert session.get('username') == 'test'  # check if the user is logged in

        response = client.get("/profile/eli", follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/profile/eli" # assert that we are directed to the profile page because we are logged in

        response = client.get("/profile/nonexistentuser", follow_redirects=True)
        assert response.status_code == 404  # assert that we get a 404 when we try to view a profile that doesn't exist