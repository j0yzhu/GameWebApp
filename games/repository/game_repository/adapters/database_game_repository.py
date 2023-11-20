import sqlite3
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.exc import IntegrityError

from games.repository.game_repository.game_repository import GameRepository
from games.repository.game_repository.adapters import csv_game_repository
from games.domainmodel.model import Genre, Game, Publisher

from games.exceptions import repository_layer_exceptions

from games.repository.orm import game_genre_relationship_table, genres_table

class DatabaseGameRepository(GameRepository):
    def __init__(self, session_context_manager):
        self.__session_context_manager = session_context_manager

    def close_session(self):
        self.__session_context_manager.close_current_session()

    def reset_session(self):
        self.__session_context_manager.reset_session()

    def get_game(self, game_id: int) -> Game:
        """
        Returns a game with the given ID
        :param game_id: The ID of the game to return
        :return: A game with the given ID
        """
        with self.__session_context_manager as session:
            try:
                game = session.session.query(Game).filter(Game._Game__game_id == game_id).one()
                return game
            except NoResultFound:
                raise repository_layer_exceptions.ResourceNotFoundException("Game with ID {} not found".format(game_id))

    def get_games_by_publisher(self, publisher: Publisher, page: int, count: int) -> List[Game]:
        """
        Returns a list of games that have the given publisher
        :param publisher: The publisher to search for
        :param page: The page number to return (offset)
        :param count: The number of results to return
        :return: A list of games that have the given publisher
        """
        with self.__session_context_manager as scm:
            games = (
                scm.session.query(Game)
                .filter(Game._Game__publisher == publisher)
                .offset((page - 1) * count)
                .limit(count)
                .all()
            )

            return games

    def get_publisher(self, publisher_name: str) -> Publisher:
        """
        Returns a publisher with the given name
        :param publisher_name: The name of the publisher to return
        :return: A publisher with the given name
        """
        with self.__session_context_manager as session:
            try:
                publisher = session.session.query(Publisher).filter(Publisher._Publisher__publisher_name == publisher_name).one()
                return publisher
            except NoResultFound:
                raise repository_layer_exceptions.ResourceNotFoundException("Publisher with name {} not found".format(publisher_name))

    def get_genre(self, genre_name: str) -> Genre:
        """
        Returns a genre with the given name (Basically just used to check if a genre exists)
        :param genre_name: The name of the genre to return
        :return: A genre with the given name
        """
        with self.__session_context_manager as session:
            try:
                genre = session.session.query(Genre).filter(Genre._Genre__genre_name == genre_name).one()
                return genre
            except NoResultFound:
                raise repository_layer_exceptions.ResourceNotFoundException("Genre with name {} not found".format(genre_name))

    def get_number_of_games(self) -> int:
        """
        Returns the number of games in the test_repository
        :return: The number of games in the test_repository
        """
        with self.__session_context_manager as scm:
            return scm.session.query(Game).count()

    def add_game(self, game: Game):
        """
        Adds a game to the test_repository
        :param game: The game to add
        """
        with self.__session_context_manager as scm:
            try:
                self.get_game(game.game_id)
                raise repository_layer_exceptions.ResourceAlreadyExistsException("Game with ID {} already exists".format(game.game_id))
            except repository_layer_exceptions.ResourceNotFoundException:
                pass

            scm.session.merge(game)
            scm.commit()

    def add_genre(self, genre: Genre):
        """
        Adds a genre to the test_repository
        :param genre: The genre to add
        """
        with self.__session_context_manager as scm:
            try:
                self.get_genre(genre.genre_name)
                raise repository_layer_exceptions.ResourceAlreadyExistsException("Genre with name {} already exists".format(genre.genre_name))
            except repository_layer_exceptions.ResourceNotFoundException:
                pass
            scm.session.add(genre)
            scm.commit()

    def get_genres(self) -> List[Genre]:
        """
        Returns a list of all genres in the test_repository
        :return: A list of all genres in the test_repository
        """
        with self.__session_context_manager as scm:
            genres = scm.session.query(Genre).all()
            return genres

    def get_publishers(self) -> List[Publisher]:
        """
        Returns a list of all publishers in the test_repository
        :return: A list of all publishers in the test_repository
        """
        with self.__session_context_manager as scm:
            publishers = scm.session.query(Publisher).all()
            return publishers

    def add_publisher(self, publisher: Publisher):
        if publisher in self.get_publishers():
            raise repository_layer_exceptions.ResourceAlreadyExistsException("Publisher with name {} already exists".format(publisher.publisher_name))

        with self.__session_context_manager as scm:
            scm.session.add(publisher)
            scm.commit()

    def search_games(self, search_term: str, page: int, count: int) -> List[Game]:
        """
        Searches for games that match the search term
        :param search_term: The term to search for
        :param page: The page number to return
        :param count: The number of results to return
        :return: A list of games that match the search term
        """
        with self.__session_context_manager as scm:
            games = (
                scm.session.query(Game)
                .filter(Game._Game__game_title.like("%{}%".format(search_term)))
                .offset((page - 1) * count)
                .limit(count)
                .all()
            )

            return games

    def get_games(self, page: int, count: int, reverse: bool) -> List[Game]:
        """
        Returns a list of games
        :param page: The page number to return (offset)
        :param count: The number of results to return
        :return: A list of games
        """
        with self.__session_context_manager as scm:
            games = scm.session.query(Game).offset((page - 1) * count).limit(count).all()
            return games

    def get_games_sorted_alphabetically(self, page: int, count: int, reverse: bool) -> List[Game]:
        """
        Returns a list of games sorted alphabetically by title
        :param page: The page number to return (offset)
        :param count: The number of results to return
        :return: A list of games sorted alphabetically by title
        """
        with self.__session_context_manager as scm:
            if not reverse:
                games = scm.session.query(Game).order_by(asc(Game._Game__game_title)).offset((page - 1) * count).limit(count).all()
            else:
                games = scm.session.query(Game).order_by(desc(Game._Game__game_title)).offset((page - 1) * count).limit(count).all()
            return games


    def get_games_sorted_by_date(self, page: int, count: int, reverse: bool) -> List[Game]:
        """
        Returns a list of games sorted by release date
        :param page: The page number to return (offset)
        :param count: The number of results to return
        :param reverse: Whether to reverse the order of the results
        :return: A list of games sorted by release date
        """
        with self.__session_context_manager as scm:
            if not reverse:
                games = scm.session.query(Game).order_by(asc(Game._Game__release_date)).offset((page - 1) * count).limit(count).all()
            else:
                games = scm.session.query(Game).order_by(desc(Game._Game__release_date)).offset((page - 1) * count).limit(count).all()
            return games

    def get_games_with_genre(self, genre: 'Genre', page: int, count: int) -> List[Game]:
        """
        Returns a list of games that have the genre in their list of genres
        :param page: The page number to return (offset)
        :param count: The number of results to return
        :param genre: The genre to search for
        :return: A list of games that have the genre in their list of genres
        """
        with self.__session_context_manager as scm:
            games = (
                scm.session.query(Game)
                .join(game_genre_relationship_table)
                .join(Genre)
                .filter(Genre._Genre__genre_name == genre.genre_name)
                .offset((page - 1) * count)
                .limit(count)
                .all()
            )

            return games

    def populate(self, testing: bool=False):

        repo = csv_game_repository.CSVGameRepository()
        repo.populate(testing)

        for game in repo.get_games(1, repo.get_number_of_games(), False):
            try:
                self.add_game(game)
            except:
                pass

        for genre in repo.get_genres():
            try:
                self.add_genre(genre)
            except:
                pass

        for publisher in repo.get_publishers():
            try:
                self.add_publisher(publisher)
            except:
                pass