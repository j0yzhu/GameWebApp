import pytest

from flask import Flask

from games.repository.wishlist_repository.adapters import csv_wishlist_repository
from games.service import wishlist_service, user_service, game_service
from games.exceptions.service_layer_exceptions import ResourceAlreadyExistsException, ResourceNotFoundException
from games.repository import user_repository, game_repository
from games.domainmodel.model import Wish, Game, User

@pytest.fixture()
def test_app():
    app = Flask(__name__)

    @app.route('/test')
    def test():
        return "test"

    app.config['SERVER_NAME'] = 'localhost'

    return app

@pytest.fixture()
def populated_wishlist_repository():
    repo = csv_wishlist_repository.CSVWishlistRepository()
    repo.populate(True)
    return repo

@pytest.fixture()
def unpopulated_wishlist_repository():
    game_repository.game_repo_instance = game_repository.csv_game_repository.CSVGameRepository()
    user_repository.user_repo_instance = user_repository.csv_user_repository.CSVUserRepository()

    return csv_wishlist_repository.CSVWishlistRepository()

@pytest.fixture()
def users():
    return [User(f'User {i}', 'password') for i in range(10)]

@pytest.fixture()
def games():
    return [Game(i+1, 'Game {i}') for i in range(10)] # i+1 because game_id must be positive

@pytest.fixture()
def wishes():
    wishes = []
    for game in [Game(i+1, 'Game {i}') for i in range(10)]:
        for user in [User(f'User {i}', 'password') for i in range(10)]:
            wishes.append(Wish(user, game))
    return wishes

def test_add_wish(unpopulated_wishlist_repository, users, games):
    for user in users: # Add a bunch of wishes, they are all considered unique
        for game in games:
            wish = Wish(user, game)
            wishlist_service.add_wish(wish, unpopulated_wishlist_repository)

    with pytest.raises(ResourceAlreadyExistsException): # try to add a duplicate wish (because user 0 and game 0 are already in the repo)
        wish = Wish(users[0], games[0])
        wishlist_service.add_wish(wish, unpopulated_wishlist_repository)

def test_remove_wish(unpopulated_wishlist_repository, wishes):
    w1 = wishes[0]
    w2 = wishes[2]

    wishlist_service.add_wish(w1, unpopulated_wishlist_repository) # add a wish to the repo

    with pytest.raises(ResourceNotFoundException): # try to remove a wish that isn't in the repo
        wishlist_service.remove_wish(w2, unpopulated_wishlist_repository)

    wishlist_service.remove_wish(w1, unpopulated_wishlist_repository) # remove a wish that is in the repo


def test_get_wishlist_by_user(unpopulated_wishlist_repository, wishes):

    for wish in wishes:
        try:
            user_service.add_user(wish.user.username, wish.user.password, user_repository.user_repo_instance)
        except:
            pass
        try:
            game_service.add_game(wish.game, game_repository.game_repo_instance)
        except:
            pass # we aren't testing the user service and game service here
        wishlist_service.add_wish(wish, unpopulated_wishlist_repository)

    user = wishes[0].user  # get a user from the list of wishes

    wishes_for_user = wishlist_service.get_wishes_by_user(user, unpopulated_wishlist_repository)  # get the wishes for that user

    assert len(wishes_for_user) == 10  # ensure that there are 10 wishes for that user
    for wish in wishes_for_user:
        assert wish.user == user  # ensure that all the wishes are for that user


def test_get_wishlist_by_game(unpopulated_wishlist_repository, wishes):
    for wish in wishes:
        try:
            user_service.add_user(wish.user.username, wish.user.password, user_repository.user_repo_instance)
        except:
            pass
        try:
            game_service.add_game(wish.game, game_repository.game_repo_instance)
        except:
            pass # we aren't testing the user service and game service here
        wishlist_service.add_wish(wish, unpopulated_wishlist_repository)

    game = wishes[0].game  # get a game from the list of wishes

    wishes_for_game = wishlist_service.get_wishes_by_game(game, unpopulated_wishlist_repository)  # get the wishes for that game

    assert len(wishes_for_game) == 10  # ensure that there are 10 wishes for that game
    for wish in wishes_for_game:
        assert wish.game == game  # ensure that all the wishes are for that game