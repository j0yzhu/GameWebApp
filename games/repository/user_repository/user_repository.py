from abc import ABC, abstractmethod, abstractproperty
from typing import List
from dataclasses import dataclass
from games.domainmodel.model import User

@dataclass(frozen=True)
class UserDTO:
    username: str
    password: str

    def __eq__(self, other):
        if not isinstance(other, (UserDTO, User)): # UserDTO and User are interchangeable
            return False
        return self.username == other.username

    def __hash__(self):
        return hash(self.username)

class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_name: str) -> User:
        return User("Example user, big fake", 'password123')

    @abstractmethod
    def get_users(self, page: int, count: int, reverse: bool) -> List[User]:
        return []

    @abstractmethod
    def get_number_of_users(self) -> int:
        return 0

    @abstractmethod
    def add_user(self, user: User):
        pass

    @abstractmethod
    def delete_user(self, user: User):
        pass

    @abstractmethod
    def populate(self, testing: bool):
        pass


def user_dto_to_user(user_dto: UserDTO) -> User:
    '''
    Converts a UserDTO object to a User object, if username_and_password_only is False, it will also populate the user's reviews, etc.
    '''
    user = User(user_dto.username, user_dto.password)

    return user
