import csv
from pathlib import Path
from typing import List
from thefuzz import fuzz

from games.repository.game_repository.game_repository import GameRepository
from games.domainmodel.model import Genre, Game, Publisher

from games.exceptions import repository_layer_exceptions

class CSVGameRepository(GameRepository):
    def __init__(self):
        self.__dataset_of_games = set()
        self.__dataset_of_publishers = set()
        self.__dataset_of_genres = set()

    def __read_csv_file(self, testing):

        if testing:

            path = Path(__file__).parent.parent / "data" / "test_games.csv"
        else:
            path = Path(__file__).parent.parent / "data" / "games.csv"

        with open(path, mode='r', encoding='utf-8-sig') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                genres = [(Genre(genre_name)) for genre_name in row["Genres"].split(",")]
                publisher = Publisher(row["Publishers"])

                game = Game(
                    game_id=int(row["AppID"]),
                    game_title=row["Name"]
                )
                game.price = float(row["Price"])
                game.release_date = row.get("Release date")
                game.description = row.get("About the game")
                game.image_url = row.get("Header image")
                game.website_url = row.get("Website")

                game.publisher = publisher
                for genre in genres:
                    game.add_genre(genre)

                self.add_game(game)

    def populate(self, testing=False):
        self.__read_csv_file(testing=testing)

    def get_number_of_games(self) -> int:
        return len(self.__dataset_of_games)

    def get_genres(self) -> List[Genre]:
        return sorted(list(self.__dataset_of_genres))

    def get_publishers(self) -> List[Publisher]:
        return list(self.__dataset_of_publishers)

    def add_publisher(self, publisher: Publisher):
        if publisher in self.__dataset_of_publishers:
            raise repository_layer_exceptions.ResourceAlreadyExistsException(f"Publisher with name {publisher.publisher_name} already exists")
        self.__dataset_of_publishers.add(publisher)

    def get_game(self, game_id: int) -> Game:
        for game in self.__dataset_of_games:
            if game.game_id == game_id:
                return game
        raise repository_layer_exceptions.ResourceNotFoundException(f"Game with ID {game_id} does not exist")

    def get_genre(self, genre_name: str) -> Genre:
        for genre in self.__dataset_of_genres:
            if genre.genre_name == genre_name:
                return genre
        raise repository_layer_exceptions.ResourceNotFoundException(f"Genre with name {genre_name} does not exist")

    def add_game(self, game: Game):
        if game in self.__dataset_of_games:
            raise repository_layer_exceptions.ResourceAlreadyExistsException(f"Game with ID {game.game_id} already exists")
        self.__dataset_of_games.add(game)

        for genre in game.genres:
            self.__dataset_of_genres.add(genre)
        if game.publisher is not None:
            self.__dataset_of_publishers.add(game.publisher)

    def get_publisher(self, publisher_name: str) -> Publisher:
        for publisher in self.__dataset_of_publishers:
            if publisher.publisher_name == publisher_name:
                return publisher
        raise repository_layer_exceptions.ResourceNotFoundException(f"Publisher with name {publisher_name} does not exist")

    def get_games_by_publisher(self, publisher: Publisher, page: int, count: int) -> List[Game]:
        if publisher not in self.__dataset_of_publishers:
            raise repository_layer_exceptions.ResourceNotFoundException(f"Publisher with name {publisher.publisher_name} does not exist")

        games = []

        for game in self.__dataset_of_games:
            if game.publisher == publisher:
                games.append(game)

        p = games[(page - 1) * count:page * count]

        return p

    def search_games(self, search_term: str, page: int, count: int) -> List['Game']:

        results = []
        for game in self.__dataset_of_games:
            results.append(
                (fuzz.token_sort_ratio(game.title.lower(), search_term.lower()), game) # Gets the ratio of similarity of the game title to the search term
            )

        results.sort(reverse=True) # Sorts the results by the ratio of similarity (Sorts tuples so if similarity is the same, the game with the higher ID is first)
        results = [x[1] for x in results] # Gets rid of the ratios

        return results[(page - 1) * count:page * count]

    def __get_games(self, page: int, count: int, sort_lambda=None, filter_lambda=None, reverse=False):
        games = list(self.__dataset_of_games)
        if filter_lambda:
            games = filter(filter_lambda, games)

        if sort_lambda:
            games = sorted(games, key=sort_lambda, reverse=reverse)
        elif reverse:
            games.reverse()  # If there is a sort function, we should reverse the order according to the sort lambda, otherwise we can just apply a reverse using the default sort method of the objects


        return list(games)[(page - 1) * count:page * count]

    def add_genre(self, genre: Genre):
        if genre in self.__dataset_of_genres:
            raise repository_layer_exceptions.ResourceAlreadyExistsException(f"Genre with name {genre.genre_name} already exists")
        self.__dataset_of_genres.add(genre)

    def get_games(self, page: int, count: int, reverse: bool=False) -> List[Game]:
        if reverse is None:
            reverse = False
        return self.__get_games(page, count, reverse=reverse)

    def get_games_sorted_by_date(self, page: int, count: int, reverse: bool=False) -> List[Game]:
        if reverse is None:
            reverse = False
        return self.__get_games(page, count, sort_lambda=lambda game: (game.get_datetime() is None, game.get_datetime(), game < game), reverse=reverse)

    def get_games_sorted_alphabetically(self, page: int, count: int, reverse=False) -> List[Game]:
        if reverse is None:
            reverse = False
        return self.__get_games(page, count, sort_lambda=lambda game: game.title.lower(), reverse=reverse)

    def get_games_with_genre(self, genre: Genre, page: int, count: int) -> List['Game']:
        if genre not in self.__dataset_of_genres:
            raise repository_layer_exceptions.ResourceNotFoundException(f"Genre with name {genre.genre_name} does not exist")

        genre_filter = lambda game: genre in game.genres  # Define the genre outside the call
        return self.__get_games(page, count, filter_lambda=genre_filter)