import pytest

from flask import Flask
from games.service import game_service
from games.domainmodel.model import Game, Genre, Publisher
from games.repository.game_repository.game_repository import GameRepository
from games.repository.game_repository.adapters import csv_game_repository
from games.exceptions import service_layer_exceptions

@pytest.fixture()
def test_app():
    app = Flask(__name__)

    @app.route('/test')
    def test():
        return "test"

    app.config['SERVER_NAME'] = 'localhost'

    return app

@pytest.fixture
def populated_game_repository():
    repo = csv_game_repository.CSVGameRepository()
    repo.populate()
    return repo


@pytest.fixture
def unpopulated_game_repository():
    return csv_game_repository.CSVGameRepository()

def test_get_game(populated_game_repository):
    game = game_service.get_game(7940, populated_game_repository) # test fetching an existing game
    assert game.game_id == 7940
    assert game.title == 'Call of Duty® 4: Modern Warfare®'  # check if game title is correct

    with pytest.raises(service_layer_exceptions.ResourceNotFoundException):
        game_service.get_game(0, populated_game_repository)  # test fetching a non-existent game

def test_add_game(unpopulated_game_repository):
    assert game_service.get_number_of_games(unpopulated_game_repository) == 0  # check if repo is empty
    game = Game(1, 'test')
    game_service.add_game(game, unpopulated_game_repository)  # add a game to the empty repo
    assert game_service.get_number_of_games(unpopulated_game_repository) == 1  # check if repo has 1 game now
    assert game_service.get_game(1, unpopulated_game_repository) == game  # check if the game we added is the same as the one we get from the repo
    game2 = Game(2, 'test2')
    game_service.add_game(game2, unpopulated_game_repository)  # add another game to the repo
    assert game_service.get_number_of_games(unpopulated_game_repository) == 2  # check if repo has 2 games now
    assert game_service.get_game(2, unpopulated_game_repository) == game2  # check if the game we added is the same as the one we get from the repo

    with pytest.raises(service_layer_exceptions.ResourceAlreadyExistsException):
        game_service.add_game(game, unpopulated_game_repository)  # test adding a game with a non-unique game_id raises an exception

    assert game_service.get_number_of_games(unpopulated_game_repository) == 2  # check if repo still has 2 games

def test_get_games(populated_game_repository, test_app):
    with test_app.app_context():
        game_page = game_service.get_games(repository=populated_game_repository, page_number=1, count=10, reverse=False, endpoint='test')
        assert len(game_page.data) == 10  # check if there are 10 games in the page
        assert game_page.has_next_page  # ensure there is a next page, since our test data has more than 10 games
        assert game_page.next_page_url == 'http://localhost/test?page=2' # ensure the next page url correctly sets the page number

def test_get_games_sorted_by_date(populated_game_repository, test_app):
    with test_app.app_context():
        game_page = game_service.get_games_sorted_by_date(repository=populated_game_repository, page_number=1, count=10, reverse=False, endpoint='test')
        assert len(game_page.data) == 10
        assert game_page.has_next_page  # ensure there is a next page, since our test data has more than 10 games
        sorted_games = sorted(game_page.data, key=lambda x: x.get_datetime())
        assert game_page.data == sorted_games  # check if the games are sorted by date

def test_get_games_sorted_alphabetically(populated_game_repository, test_app):
    with test_app.app_context():
        game_page = game_service.get_games_sorted_alphabetically(repository=populated_game_repository, page_number=1, count=10, reverse=False, endpoint='test')
        assert len(game_page.data) == 10
        assert game_page.has_next_page
        assert game_page.next_page_url == 'http://localhost/test?page=2'
        sorted_games = populated_game_repository.get_games_sorted_alphabetically(1, 10000000, False) # Get all games sorted alphabetically
        assert game_page.data == sorted_games[:10]  # check if the games are sorted by title
        reverse_game_page = game_service.get_games_sorted_alphabetically(repository=populated_game_repository, page_number=1, count=10, reverse=True, endpoint='test')
        assert reverse_game_page.data == list(reversed(sorted_games[-10:]))  # check if the games are sorted by title in reverse
        assert reverse_game_page.has_next_page

def test_get_games_by_genre(populated_game_repository, test_app):
    with test_app.app_context():
        game_page = game_service.get_games_with_genre(Genre('Action'), repository=populated_game_repository, page_number=1, count=10, reverse=False, endpoint='test')
        assert len(game_page.data) == 10
        assert game_page.has_next_page
        assert game_page.next_page_url == 'http://localhost/test?page=2'
        for game in game_page.data:
            assert Genre('Action') in game.genres  # check if all games in the page have the genre Action

def test_get_genres(unpopulated_game_repository):
    genre = Genre('Action')

    assert game_service.get_genres(unpopulated_game_repository) == []  # check if repo is empty
    game_service.add_genre(genre, unpopulated_game_repository)  # add a genre
    assert game_service.get_genres(unpopulated_game_repository) == [genre]  # check if the genre we added is in the repo
    game_service.add_genre(Genre('Adventure'), unpopulated_game_repository)  # add another genre
    assert game_service.get_genres(unpopulated_game_repository) == [genre, Genre('Adventure')] or game_service.get_genres(unpopulated_game_repository) == [Genre('Adventure'), genre]  # check if the genres are sorted alphabetically

    with pytest.raises(service_layer_exceptions.ResourceAlreadyExistsException):
        game_service.add_genre(genre, unpopulated_game_repository)  # test adding a genre with a non-unique name raises an exception

    assert game_service.get_genre('Action', unpopulated_game_repository) == genre  # test fetching an existing genre

    with pytest.raises(service_layer_exceptions.ResourceNotFoundException):
        game_service.get_genre('Non-existent-genre', unpopulated_game_repository)  # test fetching a non-existent genre