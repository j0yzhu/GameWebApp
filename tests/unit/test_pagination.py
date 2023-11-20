import pytest

from games.pagination import page
from flask import Flask
from games.domainmodel.model import Game, Genre
from games.repository.game_repository.game_repository import GameRepository
from games.repository.game_repository.adapters import csv_game_repository

@pytest.fixture()
def test_app():
    app = Flask(__name__)

    @app.route('/test')
    def test():
        return "test"

    app.config['SERVER_NAME'] = 'localhost'

    return app

@pytest.fixture()
def pagination_decorated_function():
    @page.paginated()
    def get_games_with_genre(genre: Genre, repository: GameRepository, page_number, count, reverse):
        return repository.get_games_with_genre(genre, page_number, count)

    return get_games_with_genre

@pytest.fixture()
def game_repository() -> GameRepository:
    return csv_game_repository.CSVGameRepository()
def test_pagination_decorator(test_app, pagination_decorated_function, game_repository):

    genres = [Genre("Action"), Genre("Adventure"), Genre("Indie"), Genre("RPG"), Genre("Strategy")]  # Create a bunch of genres
    id_n = 0
    for i, genre in enumerate(genres):
        game_repository.add_genre(genre)
        for j in range(0, 10):
            game = Game(id_n, f"{genre.genre_name} {id_n}")
            game.add_genre(genre)
            game_repository.add_game(game)
            id_n += 1  # add them to the test_repository

    with test_app.app_context(): # Need to do this to get the url_for function to work
        genre_page = pagination_decorated_function(genres[0], repository=game_repository, page_number=1, count=5, reverse=False, endpoint="test")  # make a page of games with genre "Action"
    assert isinstance(genre_page, page.Page)


    assert genre_page.page == 1  # check if the page number is correct
    assert genre_page.per_page == 5  # check if the number of games per page is correct
    assert len(genre_page.data) == 5  # check if the number of games in the page is correct
    assert genre_page.has_next_page == True  # check if there is a next page
    with test_app.app_context():
        assert genre_page.next_page_url == "http://localhost/test?page=2"  # check if the next page url is correct
        assert genre_page.prev_page_url == None  # check if there is no previous page

    with test_app.app_context():
        genre_page_2 = pagination_decorated_function(genres[0], repository=game_repository, page_number=2, count=5, reverse=False, endpoint="test")  # make a page of games with genre "Action" - page 2

    assert genre_page_2.page == 2  # check if the page number is correct
    assert genre_page_2.per_page == 5  # check if the number of games per page is correct
    assert len(genre_page_2.data) == 5  # check if the number of games in the page is correct
    assert genre_page_2.has_next_page == False  # check if there is no next page because we are on the last page because there are only 10 games with genre "Action"

    for game in genre_page_2:
        assert game not in genre_page.data  # check if the games in page 2 are not in page 1

    with test_app.app_context():
        assert genre_page_2.next_page_url == None  # check if the next page url is correct
        assert genre_page_2.prev_page_url == "http://localhost/test?page=1"  # check if the previous page url is correct

    with test_app.app_context():
        test_params_pages = pagination_decorated_function(genres[0], repository=game_repository, page_number=1, count=5, reverse=False, endpoint="test", example_param_1="spam", example_param_2="eggs")
        assert test_params_pages.next_page_url == "http://localhost/test?page=2&example_param_1=spam&example_param_2=eggs"  # check if urls with custom parameters are correct