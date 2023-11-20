from games.domainmodel.model import User
from games.exceptions import service_layer_exceptions, repository_layer_exceptions
from games.repository.user_repository.user_repository import UserRepository
from games.pagination.page import paginated


import bcrypt


@paginated()
def get_users(repository: UserRepository, page_number, count, reverse):
    users = repository.get_users(page_number, count, reverse)
    return users


def add_user(user_name: str, password: str, repository: UserRepository) -> User:
    '''
    Adds a user with the given user_name and password to the test_repository.

    Raises:
        NameNotUniqueException: If the user_name is already taken.
    '''

    rounds = 10

    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=rounds))
    user = User(user_name, password)

    try:
        repository.add_user(user)
    except repository_layer_exceptions.ResourceAlreadyExistsException:
        raise service_layer_exceptions.ResourceAlreadyExistsException(f"The username {user_name} is already taken")

    return user


def delete_user(user: User, repository: UserRepository):
    '''
    Deletes the given user from the test_repository.

    Raises:
        UnknownUserException: If the user does not exist.
    '''
    try:
        repository.delete_user(user)
    except repository_layer_exceptions.ResourceNotFoundException:
        raise service_layer_exceptions.ResourceNotFoundException(f"The user with the username {user.username} does not exist")


def authenticate_user(user_name: str, password: str, repository: UserRepository) -> User:
    '''
    Authenticates a user with the given user_name and password, if the combination is correct
    it will return the corresponding user object.

    Raises:
        AuthenticationException: If the username/password combination is incorrect. NOTE: Don't specify if it was the username or password that was incorrect.
    '''

    try:
        user = get_user_by_username(user_name, repository)
    except service_layer_exceptions.ResourceNotFoundException:
        raise service_layer_exceptions.AuthenticationException("Incorrect username/password combination")

    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        return user
    else:
        raise service_layer_exceptions.AuthenticationException("Incorrect username/password combination")


def get_user_by_username(username: str, repository: UserRepository) -> User:
    '''
    Returns the user with the given user_name. Because this exists on the serice layer it accesses both the user and review_repository, etc. repositories

    Raises:
        UnknownUserException: If the user does not exist.
    '''
    try:
        user = repository.get_user(username)
    except repository_layer_exceptions.ResourceNotFoundException:
        raise service_layer_exceptions.ResourceNotFoundException(f"The user with the username {username} does not exist")

    return user


def get_number_of_users(repository: UserRepository) -> int:
    return repository.get_number_of_users()


def get_logged_in_user_from_session(session, repo: UserRepository):
    if session.get('username') is None:
        return None

    try:
        user = get_user_by_username(session.get('username'), repo)
        return user
    except service_layer_exceptions.ResourceNotFoundException:
        session.pop('username') # stale username in session, we should just remove it
        return None


