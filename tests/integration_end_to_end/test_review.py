from tests.integration_end_to_end.utils import client
from flask import session, request

def test_review_form_display(client):
    with client:
        response = client.get('/')
        assert session.get('username') == None
        response = client.get('/games/game/7940', follow_redirects=True)
        assert b'Write a review' not in response.data  # assert that the review button is not showing up when we are not logged in

        response = client.post('/authentication/register', data={"user_name": "test", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True) # register a user
        assert session.get('username') == 'test'  # check if the user is logged in

        response = client.get('/games/game/7940', follow_redirects=True)
        assert b'Write a review' in response.data  # assert that the review button is showing up when we are logged in


def test_add_review(client):
    with client:
        response = client.get('/')
        assert session.get('username') == None
        response = client.post('/review/add', data={"game_id": "7940", "rating": "5", "comment": "test"}, follow_redirects=True)
        assert response.request.path == "/authentication/login" # assert that we are redirected to the login page if we aren't logged in

        response = client.post('/authentication/register', data={"user_name": "test", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True) # register a user
        assert session.get('username') == 'test'  # check if the user is logged in

        response = client.post('/review/add', data={"game_id": "7940", "rating": "5", "comment": "a very specific review for testing"}, follow_redirects=True)
        assert response.request.path == "/games/game/7940" # assert that we are redirected to the game page if we are logged in

        assert b'a very specific review for testing' in response.data  # assert that the review is in the game page

        response = client.get('/profile', follow_redirects=True)
        assert b'a very specific review for testing' in response.data # assert that the review is in the profile

        response = client.post('/review/add', data={"game_id": "7940", "rating": "6", "comment": "a very specific review for testing"}, follow_redirects=True)
        assert response.status_code == 400 # assert that we get a 400 if we try to add a review to a game that we already reviewed

        response = client.post('/review/add', data={"game_id": "7940", "rating": "5", "comment": "  "}, follow_redirects=True)
        assert response.status_code == 400 # assert that we get a 400 if we try to add a review with an empty comment

        response = client.post('/review/add', data={"game_id": "42138947123098472", "rating": "5", "comment": "a very specific review for testing"}, follow_redirects=True)
        assert response.status_code == 404 # assert that we get a 404 if we try to add a review to a game that doesn't exist