from flask import url_for, request
from typing import Iterable
from typing import Generic, List, Any, TypeVar
from games.utils import constants
from games.repository.game_repository.game_repository import GameRepository

T = TypeVar('T')

from functools import wraps

def paginated(default_reverse=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, repository, page_number=constants.DEFAULT_PAGE_NUMBER, count=constants.DEFAULT_COUNT, reverse=default_reverse, endpoint=None, **kwargs):
            if endpoint is None:
                endpoint = request.endpoint

            games = func(*args, repository=repository, page_number=page_number, count=count, reverse=reverse)
            has_next_page = func(*args, repository=repository, page_number=page_number+1, count=count, reverse=reverse) != []

            return Page(endpoint, games, page_number, count, has_next_page, **kwargs)
        return wrapper
    return decorator


class Page(Generic[T]):
    def __init__(self, endpoint: str, data: List, page: int, per_page: int, has_next_page: bool, **params):
        self.endpoint = endpoint
        self.__data = data
        self.page = page
        self.per_page = per_page
        self.has_next_page = has_next_page
        self.params = params

    @property
    def data(self):
        return self.__data

    @property
    def next_page_url(self):
        if self.has_next_page:
            return url_for(self.endpoint, page=self.page + 1, **self.params)
        else:
            return None

    @property
    def prev_page_url(self):
        if self.page > 1:
            return url_for(self.endpoint, page=self.page - 1, **self.params)
        else:
            return None

    @property
    def first_page_url(self):
        return url_for(self.endpoint, page=1, **self.params)

    @property
    def last_page_url(self):
        return url_for(self.endpoint, page=self.total_pages, **self.params)

    def __iter__(self):
        return iter(self.__data)