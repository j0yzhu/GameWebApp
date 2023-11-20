import csv
from pathlib import Path
from typing import List
from games.repository.user_repository.user_repository import UserRepository, UserDTO, user_dto_to_user
from games.domainmodel.model import User
from games.exceptions.repository_layer_exceptions import ResourceAlreadyExistsException, ResourceNotFoundException


class CSVUserRepository(UserRepository):
    def __init__(self):
        self.__dataset_of_users = set()

    def get_user(self, username: str) -> User:
        for user in self.__dataset_of_users:
            if user.username == username:
                return user_dto_to_user(user)
        raise ResourceNotFoundException(f"User with username {username} does not exist")

    def get_users(self, page: int, count: int, reverse: bool) -> List[User]:
        if page < 1:
            raise ValueError("Page number must be greater than 0")
        if count < 1:
            raise ValueError("Count must be greater than 0")

        start = (page - 1) * count
        end = start + count

        sorted_users = sorted(list(self.__dataset_of_users), key=lambda x: x.username, reverse=reverse)[start:end]
        return [user_dto_to_user(user) for user in sorted_users]

    def get_number_of_users(self) -> int:
        return len(self.__dataset_of_users)

    def add_user(self, user: User):
        if user in self.__dataset_of_users:
            raise ResourceAlreadyExistsException(f"User with username {user.username} already exists")

        user_dto = UserDTO(user.username, user.password)

        if user_dto in self.__dataset_of_users:
            raise ResourceAlreadyExistsException(f"User with username {user.username} already exists")

        self.__dataset_of_users.add(user_dto)

    def delete_user(self, user: User):
        user_dto = UserDTO(user.username, user.password)

        if user_dto not in self.__dataset_of_users:
            raise ResourceNotFoundException(f"User with username {user.username} does not exist")

        self.__dataset_of_users.remove(user_dto)

    def __read_csv_file(self, testing):
        if testing:
            path = Path(__file__).parent.parent / "data" / "test_users.csv"
        else:
            path = Path(__file__).parent.parent / "data" / "users.csv"

        with open(path, mode='r', encoding='utf-8=-sig') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                # password must be bytes
                password = row['password'].encode('utf-8')

                user = UserDTO(row['username'], password)
                self.__dataset_of_users.add(user)

    def populate(self, testing=False):
        self.__read_csv_file(testing=testing)
