from typing import List

from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import scoped_session

from games.repository.user_repository.user_repository import UserRepository
from games.domainmodel.model import User
from games.repository.user_repository.adapters import csv_user_repository

from games.exceptions import repository_layer_exceptions


class DatabaseUserRepository(UserRepository):
    def __init__(self, session_context_manager):
        self.__session_context_manager = session_context_manager

    def close_session(self):
        self.__session_context_manager.close_current_session()

    def reset_session(self):
        self.__session_context_manager.reset_session()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self.__session_context_manager.session.query(User).filter(User._User__username == user_name).one()
        except NoResultFound:
            raise repository_layer_exceptions.ResourceNotFoundException(f"User with username {user_name} does not exist.")
        return user

    def get_users(self, page: int, count: int, reverse: bool) -> List[User]:
        with self.__session_context_manager as scm:
            users = scm.session.query(User).order_by(User._User__username).offset((page-1) * count).limit(count).all()
        return users

    def get_number_of_users(self) -> int:
        with self.__session_context_manager as scm:
            num_of_users = scm.session.query(User).count()
        return num_of_users

    def add_user(self, user: User):
        try:
            self.get_user(user.username)
            raise repository_layer_exceptions.ResourceAlreadyExistsException(f"User with username {user.username} already exists")
        except repository_layer_exceptions.ResourceNotFoundException:
            pass
        with self.__session_context_manager as scm:
            scm.session.merge(user)
            scm.commit()

    def delete_user(self, user: User):
        with self.__session_context_manager as scm:
            scm.session.delete(user)
            scm.commit()

    def populate(self, testing: bool = False):
        if not testing:
            return

        repo = csv_user_repository.CSVUserRepository()
        repo.populate(testing)

        if repo.get_number_of_users() > 0:
            for user in repo.get_users(1, repo.get_number_of_users(), False):
                try:
                    self.add_user(user)
                except:
                    pass