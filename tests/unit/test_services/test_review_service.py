import pytest

from flask import Flask

from games.repository.review_repository.adapters import csv_review_repository
from games.service import review_service
from games.exceptions.service_layer_exceptions import ResourceAlreadyExistsException, ResourceNotFoundException
from games.domainmodel.model import User, Review, Game
from games.repository import game_repository, review_repository, user_repository
from games.service import game_service, user_service

@pytest.fixture()
def test_app():
    app = Flask(__name__)

    @app.route('/test')
    def test():
        return "test"

    app.config['SERVER_NAME'] = 'localhost'

    return app

@pytest.fixture()
def populated_review_repository():
    repo = csv_review_repository.CSVReviewRepository()
    repo.populate(True)

    game_repository.game_repo_instance = game_repository.csv_game_repository.CSVGameRepository()
    game_repository.game_repo_instance.populate(True)
    user_repository.user_repo_instance = user_repository.csv_user_repository.CSVUserRepository()
    user_repository.user_repo_instance.populate(True)

    return repo

@pytest.fixture()
def unpopulated_review_repository():
    game_repository.game_repo_instance = game_repository.csv_game_repository.CSVGameRepository()
    user_repository.user_repo_instance = user_repository.csv_user_repository.CSVUserRepository()

    return csv_review_repository.CSVReviewRepository()


def test_add_review(unpopulated_review_repository):
    user = User('eli', 'password')

    user_service.add_user(user.username, user.password, user_repository.user_repo_instance)

    game = Game(1, 'game')

    game_service.add_game(game, game_repository.game_repo_instance)
    review = Review(user, game, 5, 'comment')

    review_service.add_review(review, unpopulated_review_repository)

    assert review_service.get_reviews_by_user(user, unpopulated_review_repository) == [review]  # check if the review we added is the same as the one we get from the repo

    review2 = Review(user, game, 5, 'comment2') # same user and game and rating but different comment should be considered a differnet review
    review_service.add_review(review2, unpopulated_review_repository)

    assert len(review_service.get_reviews_by_user(user, unpopulated_review_repository)) == 2  # check that the repo has 2 reviews now

    review3 = Review(user, game, 4, 'comment') # same user and game and comment but different rating should be considered a same review


    with pytest.raises(ResourceAlreadyExistsException):
        review_service.add_review(review3, unpopulated_review_repository)  # test adding a review with a non-unique user, game, and comment raises an exception


    assert len(review_service.get_reviews_by_user(user, unpopulated_review_repository)) == 2  # check that the repo still has 2 reviews

def test_get_review_by_user(unpopulated_review_repository):
    game = Game(1, 'game')

    user_service.add_user('eli', 'password', user_repository.user_repo_instance)
    user = user_service.get_user_by_username('eli', user_repository.user_repo_instance)

    user_service.add_user('joy', 'password', user_repository.user_repo_instance)
    user2 = user_service.get_user_by_username('joy', user_repository.user_repo_instance)

    game_service.add_game(game, game_repository.game_repo_instance)

    review_u1_1 = Review(user, game, 5, 'comment')  # make some reviews for each user
    review_u1_2 = Review(user, game, 4, 'comment2')
    review_u2_1 = Review(user2, game, 5, 'comment')
    review_u2_2 = Review(user2, game, 4, 'comment2')

    review_service.add_review(review_u1_1, unpopulated_review_repository)  # add all the reviews
    review_service.add_review(review_u1_2, unpopulated_review_repository)
    review_service.add_review(review_u2_1, unpopulated_review_repository)
    review_service.add_review(review_u2_2, unpopulated_review_repository)

    reviews_u1 = review_service.get_reviews_by_user(user, unpopulated_review_repository)  # get reviews for each user in 2 seperate lists
    reviews_u2 = review_service.get_reviews_by_user(user2, unpopulated_review_repository)

    assert len(reviews_u1) == 2  # check that the repo has 2 reviews for user 1
    assert len(reviews_u2) == 2  # check that the repo has 2 reviews for user 2

    assert review_u1_1 in reviews_u1  # check that the repo has review 1 for user 1
    assert review_u1_2 in reviews_u1  # check that the repo has review 2 for user 1

    assert review_u2_1 in reviews_u2  # check that the repo has review 1 for user 2
    assert review_u2_2 in reviews_u2  # check that the repo has review 2 for user 2

    assert review_u1_1 not in reviews_u2  # check that the repo does not give reviews for the wrong user
    assert review_u1_2 not in reviews_u2  # check that the repo does not give reviews for the wrong user

    assert review_u2_1 not in reviews_u1  # check that the repo does not give reviews for the wrong user
    assert review_u2_2 not in reviews_u1  # check that the repo does not give reviews for the wrong user

    assert reviews_u1[0].user == user  # check that the repo gives reviews for the correct user
    assert reviews_u1[1].user == user  # check that the repo gives reviews for the correct user

    assert reviews_u2[0].user == user2  # check that the repo gives reviews for the correct user
    assert reviews_u2[1].user == user2  # check that the repo gives reviews for the correct user




def test_get_review_by_game(unpopulated_review_repository):
    user_service.add_user('eli', 'password', user_repository.user_repo_instance)
    user = user_service.get_user_by_username('eli', user_repository.user_repo_instance)

    game_1 = Game(1, 'game1')  # make some games
    game_2 = Game(2, 'game2')

    game_service.add_game(game_1, game_repository.game_repo_instance)
    game_service.add_game(game_2, game_repository.game_repo_instance)

    review_g1_1 = Review(user, game_1, 5, 'comment')  # make some reviews for each game
    review_g1_2 = Review(user, game_1, 4, 'comment2')
    review_g2_1 = Review(user, game_2, 5, 'comment')
    review_g2_2 = Review(user, game_2, 4, 'comment2')

    review_service.add_review(review_g1_1, unpopulated_review_repository)
    review_service.add_review(review_g1_2, unpopulated_review_repository)
    review_service.add_review(review_g2_1, unpopulated_review_repository)
    review_service.add_review(review_g2_2, unpopulated_review_repository)

    reviews_g1 = review_service.get_reviews_for_game(game_1, unpopulated_review_repository)  # get reviews for each game in 2 seperate lists
    reviews_g2 = review_service.get_reviews_for_game(game_2, unpopulated_review_repository)

    assert len(reviews_g1) == 2  # assert that each list only contains reviews for the relevant games and that the information is correct
    assert len(reviews_g2) == 2

    assert review_g1_1 in reviews_g1
    assert review_g1_2 in reviews_g1

    assert review_g2_1 in reviews_g2
    assert review_g2_2 in reviews_g2

    assert review_g1_1 not in reviews_g2
    assert review_g1_2 not in reviews_g2

    assert review_g2_1 not in reviews_g1
    assert review_g2_2 not in reviews_g1

    assert reviews_g1[0].game == game_1
    assert reviews_g1[1].game == game_1

    assert reviews_g2[0].game == game_2
    assert reviews_g2[1].game == game_2