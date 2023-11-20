import csv
from pathlib import Path
from typing import List
from games.repository.review_repository.review_repository import ReviewRepository, ReviewDTO

from games.domainmodel.model import User, Game, Review

from games.exceptions.repository_layer_exceptions import ResourceAlreadyExistsException, ResourceNotFoundException

from games.service.review_service import review_dto_to_review

from games.repository import game_repository
from games.repository import user_repository


class CSVReviewRepository(ReviewRepository):
    def __init__(self):
        self.__dataset_of_reviews = set()

    def get_reviews_by_user(self, user: User) -> List[Review]:
        user_reviews = []

        for review in self.__dataset_of_reviews:
            if review.username == user.username:
                user_reviews.append(review_dto_to_review(review, user_repository.user_repo_instance, game_repository.game_repo_instance, user=user))

        return user_reviews

    def get_reviews_for_game(self, game: Game) -> List[Review]:
        game_review = []

        for review in self.__dataset_of_reviews:
            if review.game_id == game.game_id:
                game_review.append(review_dto_to_review(review, user_repository.user_repo_instance, game_repository.game_repo_instance, game=game))

        return game_review

    def add_review(self, review: Review):
        review_dto = ReviewDTO(
            review.user.username,
            review.game.game_id,
            review.rating,
            review.comment
        )

        if review_dto in self.__dataset_of_reviews:
            raise ResourceAlreadyExistsException(f'Review with user <{review.user.username}> and game_id <{review.game.game_id}> and comment <{review.comment}> already exists')

        self.__dataset_of_reviews.add(review_dto)

    def __read_csv_file(self, testing):
        if testing:
            path = Path(__file__).parent.parent / "data" / "test_reviews.csv"
        else:
            path = Path(__file__).parent.parent / "data" / "reviews.csv"

        with open(path, mode='r', encoding='utf-8-sig') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                review = ReviewDTO(
                    row['username'],
                    int(row['game_id']),
                    int(row['rating']),
                    row['comment']
                )

                self.__dataset_of_reviews.add(review)

    def populate(self, testing=False):
        self.__read_csv_file(testing)
