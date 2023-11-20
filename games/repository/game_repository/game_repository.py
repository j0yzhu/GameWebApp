from abc import ABC, abstractmethod
from typing import List
from games.domainmodel.model import Genre, Game, Publisher

class GameRepository(ABC):
    @abstractmethod
    def get_game(self, game_id: int) -> Game:
        """
        Returns a game with the given ID
        :param game_id: The ID of the game to return
        :return: A game with the given ID
        """
        pass

    @abstractmethod
    def get_genre(self, genre_name: str) -> Genre:
        """
        Returns a genre with the given name (Basically just used to check if a genre exists)
        :param genre_name: The name of the genre to return
        :return: A genre with the given name
        """
        pass

    @abstractmethod
    def get_number_of_games(self) -> int:
        """
        Returns the number of games in the test_repository
        :return: The number of games in the test_repository
        """
        pass

    @abstractmethod
    def add_game(self, game: Game):
        """
        Adds a game to the test_repository
        :param game: The game to add
        """
        pass

    @abstractmethod
    def add_genre(self, genre: Genre):
        """
        Adds a genre to the test_repository
        :param genre: The genre to add
        """
        pass

    @abstractmethod
    def get_genres(self) -> List[Genre]:
        """
        Returns a list of all genres in the test_repository
        :return: A list of all genres in the test_repository
        """
        pass

    @abstractmethod
    def get_publishers(self) -> List[Publisher]:
        """
        Returns a list of all publishers in the test_repository
        :return: A list of all publishers in the test_repository
        """
        pass

    @abstractmethod
    def add_publisher(self, publisher: Publisher):
        pass

    @abstractmethod
    def get_games_by_publisher(self, publisher: Publisher, count: int, page: int) -> List[Game]:
        """
        Returns a list of games by the given publisher
        :param publisher: The publisher to search for
        :param count: The number of results to return
        :param page: The page number to return (offset)
        :return: A list of games by the given publisher
        """
        pass

    @abstractmethod
    def get_publisher(self, publisher_name: str) -> Publisher:
        """
        Returns a publisher with the given name (Basically just used to check if a publisher exists)
        :param publisher_name: The name of the publisher to return
        :return: A publisher with the given name
        """
        pass

    @abstractmethod
    def populate(self, testing: bool):
        """
        Populates the test_repository with data. May or may not be implemented depending on the test_repository type
        """
        pass

    @abstractmethod
    def search_games(self, search_term: str, page: int, count: int) -> List[Game]:
        """
        Searches for games that match the search term
        :param search_term: The term to search for
        :param page: The page number to return
        :param count: The number of results to return
        :return: A list of games that match the search term
        """
        pass

    @abstractmethod
    def get_games(self, page: int, count: int, reverse: bool) -> List[Game]:
        """
        Returns a list of all games (unsorted)
        :param page: The page number to return (offset)
        :param count: The number of results to return
        :return: A list of games
        """
        pass

    @abstractmethod
    def get_games_sorted_alphabetically(self, page: int, count: int, reverse: bool) -> List[Game]:
        """
        Returns a list of games sorted alphabetically by title
        :param page: The page number to return (offset)
        :param count: The number of results to return
        :return: A list of games sorted alphabetically by title
        """
        pass

    @abstractmethod
    def get_games_sorted_by_date(self, page: int, count: int, reverse: bool) -> List[Game]:
        """
        Returns a list of games sorted by release date
        :param page: The page number to return (offset)
        :param count: The number of results to return
        :param reverse: Whether to reverse the order of the results
        :return: A list of games sorted by release date
        """
        pass

    @abstractmethod
    def get_games_with_genre(self, genre: 'Genre', page: int, count: int) -> List[Game]:
        """
        Returns a list of games that have the genre in their list of genres
        :param page: The page number to return (offset)
        :param count: The number of results to return
        :param genre: The genre to search for
        :return: A list of games that have the genre in their list of genres
        """
        pass


