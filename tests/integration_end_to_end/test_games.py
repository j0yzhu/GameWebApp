from tests.integration_end_to_end.utils import client
from flask import session





def test_games_index(client):
    response = client.get("/games", follow_redirects=True)
    assert response.status_code == 200
    assert b"Browse Games" in response.data  # assert the games are showing up
    assert b"Call of Duty" in response.data  # assert the games are showing up

    response = client.get("/games/?page=3&count=1", follow_redirects=True)
    assert response.status_code == 200

    game_names = [b"Bartlow", b"EARTH", b"Call of Duty", b"Stalin"]

    count = 0
    for game in game_names:
        if game in response.data:
            count += 1
    assert count == 1  # assert that only one game is showing up

def test_games_search(client):
    response = client.get("/games/search?q=Call", follow_redirects=True)
    assert response.status_code == 200
    assert b"Browse Games" in response.data  # assert the games are showing up
    assert b"Call of Duty" in response.data  # assert the games are showing up


    response = client.get("/games/search")
    assert response.status_code == 400 # assert that a search without a query returns a 400

def test_games_genre(client):
    response = client.get("/games/genre/Action?page=1", follow_redirects=True)
    assert b"Call of Duty" in response.data  # assert the games are showing up

    response = client.get("/games/genre/FakeGenre?page=1", follow_redirects=True)
    assert b"Call of Duty" not in response.data  # assert games without the genre aren't showing up
    assert b"EARTH DEFENSE FORCE" in response.data # assert the games are showing up

    response = client.get("/games/genre/NonExistentGenre?page=1", follow_redirects=True)
    assert response.status_code == 404 # assert that a non-existent genre returns a 404


def test_games_game(client):
    response = client.get("/games/game/badinput", follow_redirects=True)
    assert response.status_code == 400 # check bad input returns 400 statu code

    response = client.get("/games/game/", follow_redirects=True)
    assert response.status_code == 404 # check invalid path returns 404

    response = client.get("/games/game/1", follow_redirects=True)
    assert response.status_code == 404  # check non existent game id returns 404 status code

    response = client.get("/games/game/7940", follow_redirects=True)
    assert response.status_code == 200 # assert that a non-existent game returns a 404
    assert b"Call of Duty" in response.data  # assert the games are showing up
    assert b"Add to Wishlist" not in response.data # assert add to wishlist doesn't show up when we are not logged in

    with client:
        response = client.post('/authentication/register', data={"user_name": "test", "password": "Sixsix7", "confirm_password": "Sixsix7"}, follow_redirects=True)
        assert response.status_code == 200
        assert session.get('username') == 'test'

        response = client.get("/games/game/7940", follow_redirects=True)
        assert b"Add to wishlist" in response.data  # assert add to wishlist shows up when we are logged in