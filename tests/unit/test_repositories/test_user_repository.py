import pytest
from games.domainmodel.model import User
from games.repository.user_repository.adapters import csv_user_repository
from games.exceptions.repository_layer_exceptions import ResourceAlreadyExistsException, ResourceNotFoundException
from games.repository.user_repository.user_repository import UserDTO

class TestCSVReader:
    @pytest.fixture()
    def unpopulated_user_repository(self):
        return csv_user_repository.CSVUserRepository()

    @pytest.fixture()
    def populated_user_repository(self):
        repo = csv_user_repository.CSVUserRepository()
        repo.populate(True)
        return repo

    def test_population(self, populated_user_repository):
        assert populated_user_repository.get_number_of_users() == 3 # check if there are 3 users
        assert populated_user_repository.get_user('eli') == User('eli', 'coolpassword') # check if user eli exists
        assert populated_user_repository.get_user('joy') == User('joy', 'coolerpassword')  # check if all the of users in the test data exist
        assert populated_user_repository.get_user('max') == User('max', 'coolestpassword')



    def test_get_user(self, unpopulated_user_repository):
        repo = unpopulated_user_repository
        repo.add_user(User('eli', 'password')) # add a user to the test_repository
        user = repo.get_user('eli') # test fetching an existing user
        assert isinstance(user, User)
        assert user.username == 'eli'

        with pytest.raises(ResourceNotFoundException):
            repo.get_user('non_existent_user') # test fetching a non-existent user

    def test_add_user(self, unpopulated_user_repository):
        repo = unpopulated_user_repository

        user = User('new_user', 'password') # test adding a new user
        repo.add_user(user)
        repo_user = repo.get_user('new_user')
        assert user.username == repo_user.username

        user = User('new_user_2', 'password') # test adding a user with a unique username
        repo.add_user(user)
        repo_user = repo.get_user('new_user_2')
        assert user.username == repo_user.username

        user = User('new_user', 'differnetpassword')  # test adding a user with a non-unique username
        with pytest.raises(ResourceAlreadyExistsException):
            repo.add_user(user)

    def test_delete_user(self, unpopulated_user_repository):
        repo = unpopulated_user_repository
        user = User('new_user', 'password') # test deleting an existing user
        repo.add_user(user)

        repo.delete_user(user)
        with pytest.raises(ResourceNotFoundException):
            repo.get_user('new_user')