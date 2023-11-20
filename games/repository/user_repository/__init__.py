from games.repository.user_repository.adapters import csv_user_repository
from games.repository.user_repository.user_repository import UserRepository

def create(adapter_type: str, testing: bool=False) -> UserRepository:
    if adapter_type == "csv":
        c = csv_user_repository.CSVUserRepository()

    elif adapter_type == "database":
        c = database_user_repository.DatabaseUserRepository()

    c.populate(testing)
    return c

user_repo_instance: UserRepository = None