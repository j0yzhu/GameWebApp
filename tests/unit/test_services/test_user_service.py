import pytest

from flask import Flask

from games.repository.user_repository.adapters import csv_user_repository
from games.service import user_service
from games.exceptions.service_layer_exceptions import ResourceAlreadyExistsException, ResourceNotFoundException, AuthenticationException
from games.domainmodel.model import User

@pytest.fixture()
def test_app():
    app = Flask(__name__)

    @app.route('/test')
    def test():
        return "test"

    app.config['SERVER_NAME'] = 'localhost'

    return app

@pytest.fixture()
def populated_user_repository():
    repo = csv_user_repository.CSVUserRepository()
    repo.populate(True)
    return repo

@pytest.fixture()
def unpopulated_user_repository():
    return csv_user_repository.CSVUserRepository()

def test_get_user(populated_user_repository):
    user = user_service.get_user_by_username('eli', populated_user_repository) # test fetching an existing user
    assert user.username == 'eli'
    assert user.password == b'coolpassword' # Technically the password would be hashed, but we're not testing that here

    with pytest.raises(ResourceNotFoundException):
        user_service.get_user_by_username('non_existent_user', populated_user_repository) # test fetching a non-existent user


def test_add_user(unpopulated_user_repository):
    user_service.add_user('eli', 'password', unpopulated_user_repository)  # test adding a new user
    user = user_service.get_user_by_username('eli', unpopulated_user_repository)
    assert user.username == 'eli'
    assert user_service.get_number_of_users(unpopulated_user_repository) == 1

    user_service.add_user('joy', 'password', unpopulated_user_repository)  # test adding a user with a unique username
    user = user_service.get_user_by_username('joy', unpopulated_user_repository)
    assert user.username == 'joy'
    assert user_service.get_number_of_users(unpopulated_user_repository) == 2

    with pytest.raises(ResourceAlreadyExistsException):  # test adding a user with a non-unique username
        user_service.add_user('eli', 'password', unpopulated_user_repository)
    assert user_service.get_number_of_users(unpopulated_user_repository) == 2

def test_delete_user(unpopulated_user_repository):
    repo = unpopulated_user_repository
    user = User('new_user', 'password')
    user_service.add_user(user.username, user.password, repo)  # add a user

    assert user_service.get_number_of_users(unpopulated_user_repository) == 1  # ensure the user is added
    user_service.delete_user(user, unpopulated_user_repository)  # delete the user
    assert repo.get_number_of_users() == 0  # ensure the user is deleted
    with pytest.raises(ResourceNotFoundException): # Ensure the user is deleted
        user_service.get_user_by_username('new_user', unpopulated_user_repository)  # ensure the user cant be fetched because it is deleted

    with pytest.raises(ResourceNotFoundException): # Try to delete a user that doesn't exist
        user_service.delete_user(user, unpopulated_user_repository)


def test_get_users(unpopulated_user_repository, test_app):
    for i in range(10):
        user_service.add_user(f'user{i}', 'password', unpopulated_user_repository)  # add 10 users to the repo

    with test_app.app_context():
        users_page = user_service.get_users(repository=unpopulated_user_repository, page_number=1, count=5, reverse=False, endpoint='test')  # get the first page of users
        assert users_page.has_next_page == True  # ensure there is a next page, since our test data has more than 5 users
        assert users_page.next_page_url == 'http://localhost/test?page=2'  # ensure the next page url correctly sets the page number
        assert users_page.prev_page_url == None  # ensure there is no previous page
        assert users_page.page == 1
        assert users_page.per_page == 5
        assert len(users_page.data) == 5
        users_page = user_service.get_users(repository=unpopulated_user_repository, page_number=2, count=5, reverse=False, endpoint='test')  # get the second page of users
        assert users_page.has_next_page == False
        assert users_page.next_page_url == None
        assert users_page.prev_page_url == 'http://localhost/test?page=1'
        assert users_page.page == 2
        assert users_page.per_page == 5
        assert len(users_page.data) == 5

def test_authenticate_user(unpopulated_user_repository):
    user = user_service.add_user('eli', 'password', unpopulated_user_repository)  # test adding a new user

    assert user_service.authenticate_user('eli', 'password', unpopulated_user_repository) == user  # test authenticating a user with the correct password

    with pytest.raises(AuthenticationException):
        user_service.authenticate_user('eli', 'wrongpassword', unpopulated_user_repository)  # test authenticating a user with the wrong password

    with pytest.raises(AuthenticationException):
        user_service.authenticate_user('wrongusername', 'password', unpopulated_user_repository)  # test authenticating a user with the wrong username