import pytest
import sqlalchemy
from games.repository.review_repository.review_repository import ReviewRepository
from games.repository.review_repository.adapters.database_review_repository import DatabaseReviewRepository
from games.domainmodel.model import User, Review, Game
from games.exceptions import repository_layer_exceptions

class TestDatabaseReviewRepository:
    def test_add_review(self, unpopulated_review_repository):
        review_repo = unpopulated_review_repository
        user = User("testuser", "Password1")
        game = Game(123, "Test Game")
        comment = "Great Game!"

        review = Review(user, game, 4, comment)

        review_repo.add_review(review)
        retrieved_review = review_repo.get_reviews_by_user(user)

        assert len(retrieved_review) == 1
        assert retrieved_review == [review] #in a list because we store all of our reviews in lists

    def test_get_reviews_by_game(self, populated_review_repository):
        review_repo = populated_review_repository

        game = Game(1, "Call of Duty")

        user1 = User("testuser", "Password1")
        user2 = User("testuser2", "Password2")
        user3 = User("testuser3", "Password3")

        comment = "Great Game!"

        review1 = Review(user1, game, 4, comment)
        review_repo.add_review(review1)

        review2 = Review(user2, game, 4, comment)
        review_repo.add_review(review2)

        review3 = Review(user3, game, 4, comment)
        review_repo.add_review(review3)

        retrieved_reviews = review_repo.get_reviews_for_game(game)
        assert len(retrieved_reviews) == 3
        assert retrieved_reviews == [review1, review2, review3] #in a list because we store all of our reviews in lists


    def test_get_reviews_for_game_empty(self, unpopulated_review_repository):
        review_repo = unpopulated_review_repository
        # Test when a game has no reviews
        game = Game(1, "Empty Game")
        reviews = review_repo.get_reviews_for_game(game)
        assert reviews == []

    def test_add_existing_review(self, unpopulated_review_repository):
        review_repo = unpopulated_review_repository
        # Test adding a review that already exists
        user = User("testuser", "Password1")
        game = Game(1, "Call of Duty")
        rating = 4
        comment = "Great Game!"
        review = Review(user, game, rating, comment)


        #do it once
        review_repo.add_review(review)

        #then try again to add the same review
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            review_repo.add_review(review)