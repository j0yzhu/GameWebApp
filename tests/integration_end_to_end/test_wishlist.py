from tests.integration_end_to_end.utils import client
from flask import session, request

def test_add_remove_to_wishlist(client):
    with client:
        client.get("/")
        assert session.get('username') == None
        response = client.post('/wishlist/add/7940', follow_redirects=True)
        assert response.request.path == "/authentication/login" # assert that we are redirected to the login page if we aren't logged in

        response = client.post("/authentication/register", data={"user_name": "test", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True) # register a user
        assert session.get('username') == 'test'  # check if the user is logged in

        response = client.post('/wishlist/add/7940', follow_redirects=True)
        assert response.request.path == "/games/game/7940" # assert that we are redirected to the game page if we are logged in
        assert b"Remove from wishlist" in response.data # assert that the game is in the wishlist

        response = client.post('/wishlist/add/7940', follow_redirects=True)
        assert response.status_code == 400 # assert that we get a 400 if we try to add a game to the wishlist that is already in the wishlist
        assert response.request.path == "/wishlist/add/7940" # assert that we are redirected to the game page if we are logged in

        response = client.get('/profile', follow_redirects=True)
        assert b"Call of Duty" in response.data # assert that the game is in the wishlist

        response = client.post('/wishlist/remove/7940', follow_redirects=True)
        assert response.request.path == "/games/game/7940" # assert that we are redirected to the game page if we are logged in
        assert b"Add to wishlist" in response.data # assert that the game is not in the wishlist

        response = client.get('/profile', follow_redirects=True)
        assert b"Call of Duty" not in response.data # assert that the game is not in the wishlist

        response = client.post('/wishlist/remove/7940', follow_redirects=True)
        assert response.status_code == 400 # assert that we get a 400 if we try to remove a game from the wishlist that is not in the wishlist
        assert response.request.path == "/wishlist/remove/7940" # assert that we are not redirected to the game page if failed, (its showing an error page)