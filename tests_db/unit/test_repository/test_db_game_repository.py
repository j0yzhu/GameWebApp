import pytest

from games.repository.game_repository.adapters import database_game_repository
from games.repository.orm import SessionContextManager
from games.domainmodel.model import Game, Publisher, Genre, User, Review, Wishlist
from games.repository import game_repository
from games.__init__ import create_app

from games.exceptions import repository_layer_exceptions

from games.config import Config

class TestDatabase:
    def test_population(self, populated_game_repository):
        game_repo = populated_game_repository

        assert game_repo.get_number_of_games() == 4
        game = game_repo.get_game(7940)
        assert game.title == "Call of Duty® 4: Modern Warfare®"
        assert game.publisher == Publisher("Activision")
        assert Genre("Action") in game.genres

        genre = game_repo.get_genre('Action')
        assert genre.genre_name == 'Action'

        publisher = game_repo.get_publishers()

        assert Publisher("Activision") in publisher

    def test_add_game(self, unpopulated_game_repository):
        game_repo = unpopulated_game_repository

        game = Game(1234, "Test Game")
        game.price = 10
        game.release_date = "Oct 10, 2021"
        game_repo.add_game(game)
        assert game_repo.get_number_of_games() == 1
        assert game_repo.get_game(1234) == game

        with pytest.raises(repository_layer_exceptions.ResourceAlreadyExistsException):
            game_repo.add_game(game)


    def test_add_genre(self, unpopulated_game_repository):
        game_repo = unpopulated_game_repository

        genre = Genre("Test Genre")
        game_repo.add_genre(genre)
        assert game_repo.get_genre("Test Genre") == genre

        with pytest.raises(repository_layer_exceptions.ResourceAlreadyExistsException):
            game_repo.add_genre(genre)

    def test_get_game(self, populated_game_repository):
        game_repo = populated_game_repository
        game = game_repo.get_game(7940) # test can fetch game
        assert game.title == "Call of Duty® 4: Modern Warfare®"
        assert game.publisher == Publisher("Activision")
        assert Genre("Action") in game.genres # test it also fetches the genre of the game

        with pytest.raises(repository_layer_exceptions.ResourceNotFoundException): # test for non-existent game
            game_repo.get_game(1234)

    def test_get_genre(self, populated_game_repository):
        game_repo = populated_game_repository

        genre = game_repo.get_genre("Action")
        assert genre.genre_name == "Action"

        with pytest.raises(repository_layer_exceptions.ResourceNotFoundException):
            game_repo.get_genre("Test Genre")

    def test_get_games_with_genre(self, unpopulated_game_repository):
        game_repo = unpopulated_game_repository

        genre1 = Genre("Test Genre 1")
        genre2 = Genre("Test Genre 2")
        genre3 = Genre("Test Genre 3")

        game_repo.add_genre(genre1)
        game_repo.add_genre(genre2)

        game1 = Game(1234, "Test Game 1")
        game2 = Game(1235, "Test Game 2")
        game3 = Game(1236, "Test Game 3")
        game4 = Game(1237, "Test Game 4")

        game1.add_genre(genre1)
        game2.add_genre(genre1)
        game3.add_genre(genre2)
        game4.add_genre(genre2)

        game2.add_genre(genre2)

        game_repo.add_game(game1)
        game_repo.add_game(game2)
        game_repo.add_game(game3)
        game_repo.add_game(game4)

        assert sorted(game_repo.get_games_with_genre(genre1, 1, 10)) == sorted([game1, game2])
        assert sorted(game_repo.get_games_with_genre(genre2, 1, 10)) == sorted([game2, game3, game4])
        assert sorted(game_repo.get_games_with_genre(genre3, 1, 10)) == sorted([])

    def test_search_games(self, unpopulated_game_repository):
        game_repo = unpopulated_game_repository

        game1 = Game(1234, "Test Game 1")
        game2 = Game(1235, "Test Game 2")
        game3 = Game(1236, "Test Game 3")
        game4 = Game(1237, "Test Game 4")

        game_repo.add_game(game1)
        game_repo.add_game(game2)
        game_repo.add_game(game3)
        game_repo.add_game(game4)

        assert sorted(game_repo.search_games("Test Game", 1, 10)) == sorted([game1, game2, game3, game4])
        assert sorted(game_repo.search_games("Test Game 1", 1, 10)) == sorted([game1])
        assert sorted(game_repo.search_games("fajskdfj02ijfsa", 1, 10)) == sorted([])

    def test_get_games_sorted_alphabetically(self, unpopulated_game_repository):
        game_repo = unpopulated_game_repository

        for i, char in enumerate("asdfjaoiwjvlszcnvidfjeowiajsdlkfjazxvcafsad"):
            game = Game(i, char)
            game_repo.add_game(game)



        assert game_repo.get_games_sorted_alphabetically(1, 15, False) == sorted([game for game in game_repo.get_games(1, 1000, False)], key=lambda game: game.title)[:15]

    def test_get_games_sorted_by_date(self, unpopulated_game_repository):
        game_repo = unpopulated_game_repository

        for i in range(0, 10):
            game = Game(i, "Test Game {}".format(i))
            game.release_date = "Oct 10, 202{}".format(i)
            game_repo.add_game(game)

        date_sorted_games = game_repo.get_games_sorted_by_date(1, 1000, False)
        assert date_sorted_games == sorted(date_sorted_games, key=lambda game: game.release_date)