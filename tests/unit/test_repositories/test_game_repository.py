import pytest

from games.domainmodel.model import Game

from games.repository import game_repository
from games.repository.game_repository.game_repository import GameRepository
from games.domainmodel.model import *
from games.exceptions import repository_layer_exceptions

from games.repository.game_repository.adapters import csv_game_repository

def test_create_repository():
    repo = game_repository.create('csv')
    assert isinstance(repo, GameRepository)



# Unit tests for CSVReader
class TestCSVReader:
    @pytest.fixture()
    def populated_csv_game_repository(self):
        repo = csv_game_repository.CSVGameRepository()
        repo.populate()
        return repo

    @pytest.fixture()
    def unpopulated_csv_game_repository(self):
        return csv_game_repository.CSVGameRepository()

    def test_populate(self, unpopulated_csv_game_repository):
        assert len(unpopulated_csv_game_repository.get_games(1, 10)) == 0  # check if repo is empty
        unpopulated_csv_game_repository.populate()  # populate repo
        assert len(unpopulated_csv_game_repository.get_games(1, 10)) > 0  # check if repo is not empty

    def test_games_dataset(self, populated_csv_game_repository):
        game = populated_csv_game_repository.get_games(1, 10)[0]  # get first game
        assert isinstance(game.game_id, int) # check if game_id is an int
        assert isinstance(game.title, str) # check if title is a string
        assert isinstance(game.price, (float, int))  # check if price is a float or int
        assert isinstance(game.release_date, str)  # check if release_date is a string
        assert isinstance(game.publisher, Publisher)  # check if publisher is a Publisher
        assert isinstance(game.genres, list)  # check if genres is a list
        assert isinstance(game.description, str)  # check if description is a string

    def test_publisher_dataset(self, populated_csv_game_repository):
        publisher = populated_csv_game_repository.get_publishers()[0]  # get first publisher
        assert isinstance(publisher.publisher_name, str)  # check if publisher_name is a string

    def test_genres_dataset(self, populated_csv_game_repository):
        genre = populated_csv_game_repository.get_genres()[0]  # get first genre
        assert isinstance(genre.genre_name, str)  # check if genre_name is a string

    def test_get_game(self, populated_csv_game_repository):
        game = populated_csv_game_repository.get_game(7940)  # get game with id 7940
        assert isinstance(game, Game)  # check if game is a Game
        assert game.game_id == 7940  # check if game_id is 7940
        assert game.publisher == Publisher("Activision")  # check if publisher is Activision

        with pytest.raises(repository_layer_exceptions.ResourceNotFoundException):
            populated_csv_game_repository.get_game(1234567890123456789)  # check if exception is raised when game_id is not found

    def test_get_games(self, unpopulated_csv_game_repository):
        repo = unpopulated_csv_game_repository

        games = [Game(i, f"Game {i}") for i in range(1, 20)]  # create 19 games

        for game in games:
            repo.add_game(game)  # add games to repo

        # the games use a set internally, so the order is not guaranteed

        games_from_repo = repo.get_games(1, 20)  # get all games from repo
        assert len(games_from_repo) == 19  # check if all games are returned
        assert sorted(games_from_repo, key=lambda x: x.game_id) == games  # check if the games match the ones we made originally


    def test_search(self, populated_csv_game_repository):
        repo = populated_csv_game_repository
        results = repo.search_games("call of duty", 1, 10)  # search for call of duty
        assert 'call of duty' in results[0].title.lower()  # check if call of duty is in the first result

    def test_games_sorted_alphabetically(self, unpopulated_csv_game_repository):
        repo = unpopulated_csv_game_repository
        game1 = Game(1, "A")  # create 3 games
        game2 = Game(2, "B")
        game3 = Game(3, "C")
        repo.add_game(game2)  # add games to repo
        repo.add_game(game1)
        repo.add_game(game3)
        sorted_games = repo.get_games_sorted_alphabetically(1, 10, False)  # get games sorted alphabetically
        assert sorted_games == [game1, game2, game3]  # check if games are sorted alphabetically
        reverse_sorted_games = repo.get_games_sorted_alphabetically(1, 10, True)
        assert reverse_sorted_games == [game3, game2, game1]  # check if games are sorted alphabetically in reverse

    def test_games_sorted_by_date(self, unpopulated_csv_game_repository):
        repo = unpopulated_csv_game_repository
        game0 = Game(5, "A")
        game1 = Game(1, "A")
        game1.release_date = "Oct 21, 2008"
        game2 = Game(2, "B")
        game2.release_date = "Nov 15, 2010"
        game3 = Game(3, "C")
        game3.release_date = "Mar 18, 2015"
        game4 = Game(4, "D")  # create 5 games with different release dates and some null release dates
        repo.add_game(game0)
        repo.add_game(game1)
        repo.add_game(game4)
        repo.add_game(game3)
        repo.add_game(game2)
        sorted_games = repo.get_games_sorted_by_date(1, 10, False)
        assert sorted_games == [game1, game2, game3, game4, game0]  # check if games are sorted by date
        assert game4.release_date == None
        reverse_sorted_games = repo.get_games_sorted_by_date(1, 10, True)
        assert reverse_sorted_games == [game4, game0, game3, game2, game1]  # check if games are sorted by date in reverse

    def test_get_games_with_genre(self, unpopulated_csv_game_repository):
        repo = unpopulated_csv_game_repository

        action = Genre("Action")
        rpg = Genre("RPG")
        adventure = Genre("Adventure")
        gore = Genre("Gore")

        game0 = Game(1, "A")
        game0.add_genre(action)

        game1 = Game(2, "B")
        game1.add_genre(action)

        game2 = Game(3, "C")
        game2.add_genre(action)

        game3 = Game(4, "D")
        game3.add_genre(rpg)

        game4 = Game(5, "E")
        game4.add_genre(adventure)

        repo.add_game(game0)
        repo.add_game(game1)
        repo.add_game(game2)
        repo.add_game(game3)
        repo.add_game(game4)

        """Error finding please ignore
        
        for game in repo.games:
            print(game.title, game.genres)
        """

        action_games = repo.get_games_with_genre(action, 1, 10)
        for game in action_games:
            assert action in game.genres  # check if all games have the action genre

        sorted_genres_games = repo.get_games_with_genre(action, 1, 10)
        assert sorted_genres_games == [game0, game1, game2]  # Getting all the action games, which is game 1, 2 and 3

        sorted_genres_games = repo.get_games_with_genre(adventure, 1, 10)
        assert sorted_genres_games == [game4]  # Having a genre with just 1 game in it should return only 1 game

        with pytest.raises(repository_layer_exceptions.ResourceNotFoundException):
            sorted_genres_games = repo.get_games_with_genre(gore, 1, 10)
            # assert sorted_genres_games == []   # No games of a genre should make empty list

        repo = csv_game_repository.CSVGameRepository()
        repo.populate()

        free_genre = repo.get_genre("Free to Play")
        assert free_genre == Genre("Free to Play")
        free_games = repo.get_games_with_genre(free_genre, 1, 10)
        for game in free_games:
            assert free_genre in game.genres  # check if all games have the free to play genre