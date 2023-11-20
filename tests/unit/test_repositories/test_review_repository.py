import pytest
from games.domainmodel.model import Review, User, Game
from games.repository.review_repository.review_repository import ReviewDTO
from games.repository.review_repository.adapters import csv_review_repository

from games.repository import user_repository, game_repository

class TestCSVReader:
    @pytest.fixture()
    def unpopulated_review_repository(self):
        user_repository.user_repo_instance = user_repository.csv_user_repository.CSVUserRepository()
        game_repository.game_repo_instance = game_repository.csv_game_repository.CSVGameRepository()
        return csv_review_repository.CSVReviewRepository()

    @pytest.fixture()
    def populated_review_repository(self):
        user_repository.user_repo_instance = user_repository.csv_user_repository.CSVUserRepository()
        game_repository.game_repo_instance = game_repository.csv_game_repository.CSVGameRepository()
        game_repository.game_repo_instance.populate(True)


        repo = csv_review_repository.CSVReviewRepository()
        repo.populate(True)
        return repo
    def test_population(self, populated_review_repository):
        """
        Test if when we populate from CSV, there is some data
        """

        u1 = User('max', 'password')
        u2 = User('eli', 'password')
        u3 = User('joy', 'password')


        user_repository.user_repo_instance.add_user(u1)
        user_repository.user_repo_instance.add_user(u2)
        user_repository.user_repo_instance.add_user(u3)

        # use get_review_by_user
        reviews_1 = populated_review_repository.get_reviews_by_user(u1)
        reviews_2 = populated_review_repository.get_reviews_by_user(u2)
        reviews_3 = populated_review_repository.get_reviews_by_user(u3)

        # assert that the reviews we retrieve match the ones in test_reviews.csv
        assert reviews_1[0].user == u1
        assert reviews_1[0].game == Game(1228870, "blah")
        assert reviews_1[0].rating == 1
        assert reviews_1[0].comment == "bad game"

        assert reviews_2[0].user == u2
        assert reviews_2[0].game == Game(7940, "blah")
        assert reviews_2[0].rating == 5
        assert reviews_2[0].comment == "good game"


    def test_reviews_by_user(self, unpopulated_review_repository):
        # make a user
        u1 = User('eli','password')
        u2 = User('max', 'password')
        u3 = User('joy', 'password')


        user_repository.user_repo_instance.add_user(u1)
        user_repository.user_repo_instance.add_user(u2)
        user_repository.user_repo_instance.add_user(u3)


        game = Game(10, "Game")
        game_repository.game_repo_instance.add_game(game)

        # make some reviews by the user
        reviews_by_u1 = [Review(u1, game, i%5, f"Review {i}") for i in range(10)]
        reviews_by_u2 = [Review(u2, game, i%5, f"Review {i}") for i in range(10)]
        reviews_by_u3 = [Review(u3, game, i%5, f"Review {i}") for i in range(10)]

        # add all the reviews to the review test_repository
        for review in reviews_by_u1 + reviews_by_u2 + reviews_by_u3:
            unpopulated_review_repository.add_review(review)

        # fetch the reviews by each user and assert that they only belong to that user (check the username)
        fetched_reviews_by_u1 = unpopulated_review_repository.get_reviews_by_user(u1)
        for review in fetched_reviews_by_u1:
            assert review.user.username == u1.username
        assert len(fetched_reviews_by_u1) == 10

        fetched_reviews_by_u2 = unpopulated_review_repository.get_reviews_by_user(u2)
        for review in fetched_reviews_by_u2:
            assert review.user.username == u2.username
        assert len(fetched_reviews_by_u2) == 10

        fetched_reviews_by_u3 = unpopulated_review_repository.get_reviews_by_user(u3)
        for review in fetched_reviews_by_u3:
            assert review.user.username == u3.username
        assert len(fetched_reviews_by_u3) == 10

    def test_reviews_by_game(self, unpopulated_review_repository):
        # make a user
        u1 = User('eli','password')
        u2 = User('max', 'password')
        u3 = User('joy', 'password')

        user_repository.user_repo_instance.add_user(u1)
        user_repository.user_repo_instance.add_user(u2)
        user_repository.user_repo_instance.add_user(u3)

        g1 = Game(1, "Game")
        game_repository.game_repo_instance.add_game(g1)
        g2 = Game(2, "Game")
        game_repository.game_repo_instance.add_game(g2)
        g3 = Game(3, "Game")
        game_repository.game_repo_instance.add_game(g3)

        # make some reviews by the user
        for user in (u1, u2, u3):
            for game in (g1, g2, g3):
                    unpopulated_review_repository.add_review(Review(user, game, 4, f"Review by {u1}"))

        # fetch the reviews by each user and assert that they only belong to that user (check the username)
        fetched_reviews_by_g1 = unpopulated_review_repository.get_reviews_for_game(g1)
        for review in fetched_reviews_by_g1:
            assert review.game.game_id == g1.game_id

        fetched_reviews_by_g2 = unpopulated_review_repository.get_reviews_for_game(g2)
        for review in fetched_reviews_by_g2:
            assert review.game.game_id == g2.game_id

        fetched_reviews_by_g3 = unpopulated_review_repository.get_reviews_for_game(g3)
        for review in fetched_reviews_by_g3:
            assert review.game.game_id == g3.game_id