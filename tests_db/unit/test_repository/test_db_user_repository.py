import pytest

from games.repository.user_repository.adapters import database_user_repository
from games.repository.orm import SessionContextManager
from games.domainmodel.model import User
from games.repository import user_repository
from games.__init__ import create_app

from games.exceptions import repository_layer_exceptions

from games.config import Config

class TestDatabase:
    def test_population(self, populated_user_repository):
        user_repo = populated_user_repository

        #check num users
        num_users = user_repo.get_number_of_users()
        assert num_users > 0

        #is in populated data
        user = user_repo.get_user("joy")
        assert user is not None
        assert user.username == 'joy'

    def test_get_user(self, populated_user_repository):
        user_repo = populated_user_repository

        # is in populated data
        user = user_repo.get_user("joy")
        assert user is not None
        assert user.username == 'joy'

        # test for nonexistent user
        with pytest.raises(repository_layer_exceptions.ResourceNotFoundException):
            user_repo.get_user("nonexistent_user")
    def test_get_users(self, populated_user_repository):
        user_repo = populated_user_repository

        users = user_repo.get_users(page=1, count=10, reverse=False)
        assert len(users) > 0
    def test_get_number_of_users(self, populated_user_repository):
        user_repo = populated_user_repository

        num_users = user_repo.get_number_of_users()
        assert num_users > 0
    def test_add_user(self, unpopulated_user_repository):
        user_repo = unpopulated_user_repository

        # adding new user
        new_user = User(username='eli', password='new_password')
        user_repo.add_user(new_user)

        # checking if user is in populated data
        retrieved_user = user_repo.get_user('eli')
        assert retrieved_user == new_user

        # test for adding same user again
        with pytest.raises(repository_layer_exceptions.ResourceAlreadyExistsException):
            user_repo.add_user(new_user)

    def test_delete_user(self, populated_user_repository):
        user_repo = populated_user_repository

        # is in populated data
        user = user_repo.get_user("joy")
        assert user is not None
        assert user.username == ("joy")

        # delete user
        user_repo.delete_user(user)

        # test for getting deleted user
        with pytest.raises(repository_layer_exceptions.ResourceNotFoundException):
            user_repo.get_user("joy")




