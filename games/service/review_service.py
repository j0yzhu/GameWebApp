from games.domainmodel.model import Review, User, Game
from typing import List
from games.service import game_service, user_service
from games.repository.review_repository.review_repository import ReviewDTO, ReviewRepository
from games.exceptions import service_layer_exceptions, repository_layer_exceptions

from games.repository import game_repository as gr, user_repository as ur


def get_reviews_by_user(user: User, review_repository: ReviewRepository) -> List[Review]:
    '''
    Returns a list of all reviews written by the given user
    '''

    reviews = review_repository.get_reviews_by_user(user)
    return reviews


def get_reviews_for_game(game: Game, review_repository: ReviewRepository) -> List[Review]:
    '''
    Returns a list of all reviews written for the given game
    '''
    reviews = review_repository.get_reviews_for_game(game)
    return reviews

def add_review(review: Review, review_repository: ReviewRepository):
    '''
    Adds a review to the given review_repository
    '''
    try:
        review_repository.add_review(review)
    except repository_layer_exceptions.ResourceAlreadyExistsException:
        raise service_layer_exceptions.ResourceAlreadyExistsException(f'Review with user <{review.user.username}> and game_id <{review.game.game_id}> and comment <{review.comment}> already exists')

def review_dto_to_review(review_dto: ReviewDTO, user_repository: ur.UserRepository, game_repository: gr.GameRepository, user=None, game=None) -> Review:
    '''
    Converts a ReviewDTO to a Review
    '''

    user = user if user else user_service.get_user_by_username(review_dto.username, user_repository) # Get the user if it's not provided
    game = game if game else game_service.get_game(review_dto.game_id, game_repository) # Get the game if it's not provided



    review = Review(
        user=user,
        game=game,
        rating = review_dto.rating,
        comment=review_dto.comment,
    )

    return review