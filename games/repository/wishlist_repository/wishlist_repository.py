from abc import ABC, abstractmethod
from typing import List
from games.domainmodel.model import User, Game, Wish
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WishDTO():
    username: str
    game_id: int
    wish_time: datetime.date

    def __hash__(self):
        return hash((self.username, self.game_id))

    def __eq__(self, other):
        if not isinstance(other, WishDTO):
            return False
        return self.username == other.username and self.game_id == other.game_id

class WishlistRepository(ABC):

    @abstractmethod
    def get_wishlist_by_user(self, user: User) -> List[Wish]:
        """
        Retrieves the wishlist for a specific user.
        :param user: the user object
        :return: list of games in the user's wishlist
        """
        return []

    @abstractmethod
    def get_wishlist_by_game(self, game: Game) -> List[Wish]:
        """
        Retrieves the wishlist for a specific user.
        :param user: the user object
        :return: list of games in the user's wishlist
        """
        return []
    @abstractmethod
    def add_wish(self, wish: Wish):
        """
        Adds a game to a user's wishlist.
        :param user: the user object
        :param game: the game object
        """
        pass

    @abstractmethod
    def remove_wish(self, wish: Wish):
        """
        Removes a game from a user's wishlist.
        :param user: the user object
        :param game: the game object
        """
        pass

    @abstractmethod
    def populate(self, testing: bool=False):
        """
        Populates the test_repository with games
        """