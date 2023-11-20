from games.repository.game_repository.game_repository import GameRepository
from games.repository.game_repository.adapters import csv_game_repository


def create(adapter_type: str, testing: bool=False) -> GameRepository:
    if adapter_type == "csv":
        c = csv_game_repository.CSVGameRepository()

    elif adapter_type == "database":
        c = database_game_repository.DatabaseGameRepository()
    else:
        raise ValueError("Invalid adapter type specified")

    c.populate(testing)
    return c

game_repo_instance: GameRepository = None