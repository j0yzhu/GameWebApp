from games.domainmodel.model import Game, Genre

from games.repository.game_repository.game_repository import GameRepository
from games.exceptions import repository_layer_exceptions, service_layer_exceptions

from flask import request
from games.utils import constants
from games.pagination.page import paginated

def get_game(game_id: int, game_repository: GameRepository):
    try:
        return game_repository.get_game(game_id)
    except repository_layer_exceptions.ResourceNotFoundException:
        raise service_layer_exceptions.ResourceNotFoundException(f"Game with ID {game_id} not found")

def add_game(game: Game, game_repository: GameRepository):
    try:
        game_repository.add_game(game)
    except repository_layer_exceptions.ResourceAlreadyExistsException:
        raise service_layer_exceptions.ResourceAlreadyExistsException(f"Game with ID {game.game_id} already exists")

@paginated()
def get_games(repository: GameRepository, page_number, count, reverse):
    return repository.get_games(page_number, count, reverse)

def get_number_of_games(repository: GameRepository):
    return repository.get_number_of_games()
def get_genres(repository: GameRepository):
    return repository.get_genres()

def get_genre(genre_name: str, repository: GameRepository):
    try:
        return repository.get_genre(genre_name)
    except repository_layer_exceptions.ResourceNotFoundException:
        raise service_layer_exceptions.ResourceNotFoundException(f"Genre with name {genre_name} not found")


def add_genre(genre: Genre, repository: GameRepository):
    try:
        repository.add_genre(genre)
    except repository_layer_exceptions.ResourceAlreadyExistsException:
        raise service_layer_exceptions.ResourceAlreadyExistsException(f"Genre with name {genre.genre_name} already exists")


def get_publishers(repository: GameRepository):
    return repository.get_publishers()

def get_publisher(publisher_name: str, repository: GameRepository):
    try:
        return repository.get_publisher(publisher_name)
    except repository_layer_exceptions.ResourceNotFoundException:
        raise service_layer_exceptions.ResourceNotFoundException(f"Publisher with name {publisher_name} not found")

@paginated()
def get_games_by_publisher(publisher, repository: GameRepository, page_number, count, reverse):
    return repository.get_games_by_publisher(publisher, page_number, count)

@paginated()
def search_games(search_term: str, repository: GameRepository, page_number, count, reverse):
    return repository.search_games(search_term, page_number, count)

@paginated()
def get_games_with_genre(genre: Genre, repository: GameRepository, page_number, count, reverse):
    return repository.get_games_with_genre(genre, page_number, count)


@paginated(default_reverse=True)
def get_games_sorted_by_date(repository: GameRepository, page_number, count, reverse):
    return repository.get_games_sorted_by_date(page_number, count, reverse)

@paginated()
def get_games_sorted_alphabetically(repository: GameRepository, page_number, count, reverse):
    return repository.get_games_sorted_alphabetically(page_number, count, reverse)

