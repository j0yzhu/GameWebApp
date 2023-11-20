from typing import List

from games.repository.review_repository.review_repository import ReviewRepository
from games.domainmodel.model import User, Game, Review
from games.repository.review_repository.adapters import csv_review_repository
from games.repository.user_repository.adapters import csv_user_repository
from games.repository.game_repository.adapters import csv_game_repository
from games.repository import user_repository, game_repository

from games.exceptions import repository_layer_exceptions

class DatabaseReviewRepository(ReviewRepository):
    def __init__(self, session_context_manager):
        self.__session_context_manager = session_context_manager

    def close_session(self):
        self.__session_context_manager.close_current_session()

    def reset_session(self):
        self.__session_context_manager.reset_session()

    def get_reviews_by_user(self, user: User) -> List[Review]:
        with self.__session_context_manager as scm:
            user_reviews = (
                scm.session.query(Review)
                .join(User)
                .filter(User._User__username == user.username)
                .all()
            )
            return user_reviews

    def get_reviews_for_game(self, game: Game) -> List[Review]:
        with self.__session_context_manager as scm:
            game_reviews = (
                scm.session.query(Review)
                .filter(Review.game_id == game.game_id)
                .all()
            )
            return game_reviews

    def get_review(self, game: Game, user: User, comment: str):
        with self.__session_context_manager as scm:
            try:
                review = (
                    scm.session.query(Review)
                    .join(User)
                    .filter(Review._Review__game == game)
                    .filter(Review._Review__user == user)
                    .filter(Review._Review__comment == comment)
                    .one()
                )
                return review
            except:
                raise repository_layer_exceptions.ResourceNotFoundException(f"Review with game {game.game_id}, user {user.username} and comment {comment} not found")

    def add_review(self, review: Review):
        with self.__session_context_manager as scm:
            try:
                scm.session.expunge(review)
            except: # If the review is not in the session
                pass

        try:
            r = self.get_review(review.game, review.user, review.comment)
            raise repository_layer_exceptions.ResourceAlreadyExistsException(f"Review with game {review.game.game_id}, user {review.user.username} and comment {review.comment} already exists")
        except repository_layer_exceptions.ResourceNotFoundException:
            pass

        with self.__session_context_manager as scm:
            scm.session.merge(review)
            scm.commit()


    def populate(self, testing: bool=False):
        """
        Populates the repository with games
        """

        if not testing:
            return

        repo = csv_review_repository.CSVReviewRepository()
        repo.populate(testing)


        old_user_repo_instance = user_repository.user_repo_instance
        old_game_repo_instance = game_repository.game_repo_instance

        user_repo = csv_user_repository.CSVUserRepository()
        game_repo = csv_game_repository.CSVGameRepository()
        user_repo.populate(testing)
        game_repo.populate(testing)

        user_repository.user_repo_instance = user_repo
        game_repository.game_repo_instance = game_repo


        for user in user_repo.get_users(1, user_repo.get_number_of_users(), False):
            for review in repo.get_reviews_by_user(user):
                try:
                    with self.__session_context_manager as scm:
                        game = scm.session.query(Game).filter(Game._Game__game_id == review.game.game_id).one()
                        user = scm.session.query(User).filter(User._User__username == review.user.username).one()
                    review._Review__game = game
                    review._Review__user = user
                    self.add_review(review)
                except:
                    pass

        user_repository.user_repo_instance = old_user_repo_instance
        game_repository.game_repo_instance = old_game_repo_instance