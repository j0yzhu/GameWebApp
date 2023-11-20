from abc import ABC, abstractmethod
from typing import List
from games.domainmodel.model import User, Game, Review
from dataclasses import dataclass

@dataclass(frozen=True)
class ReviewDTO:
    username: str
    game_id: int
    rating: int
    comment: str

    def __eq__(self, other):
        if isinstance(other, ReviewDTO):
            return other.username == self.username and other.game_id == self.game_id and other.comment == self.comment
        return False

    def __hash__(self):
        return hash((self.username, self.game_id, self.comment))

class ReviewRepository(ABC):

    @abstractmethod
    def get_reviews_by_user(self, user: User) -> List[Review]:
        """
        :param user: the user object
        :return: reviews written by the specific username
        """
        pass
    @abstractmethod
    def get_reviews_for_game(self, game: Game) -> List[Review]:
        """
        :param game: the game object
        :return: reviews for the specific game
        """

    @abstractmethod
    def add_review(self, review: Review):
        """
        Adds review_repository to the test_repository
        :param review: the review_repository object
        """

    @abstractmethod
    def populate(self, testing: bool=False):
        """
        Populates the test_repository with games
        """