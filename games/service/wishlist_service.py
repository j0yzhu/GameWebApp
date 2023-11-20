from games.repository import game_repository as gr, user_repository as ur
from games.repository.wishlist_repository.wishlist_repository import WishlistRepository, WishDTO
from games.domainmodel.model import User, Wish, Game
from games.exceptions import repository_layer_exceptions, service_layer_exceptions
from games.service import user_service, game_service
from typing import List

def add_wish(wish: Wish, repo: WishlistRepository):
    try:
        repo.add_wish(wish)
    except repository_layer_exceptions.ResourceAlreadyExistsException:
        raise service_layer_exceptions.ResourceAlreadyExistsException("Wish already exists in test_repository")


def remove_wish(wish: Wish, repo: WishlistRepository):
    try:
        repo.remove_wish(wish)
    except repository_layer_exceptions.ResourceNotFoundException:
        raise service_layer_exceptions.ResourceNotFoundException("Wish does not exist in the test_repository so cannot be removed")

def get_wishes_by_user(user: User, repo: WishlistRepository) -> List[Wish]:
    wishes = repo.get_wishlist_by_user(user)

    return wishes

def get_wishes_by_game(game: Game, repo: WishlistRepository) -> List[Wish]:
    wishes = repo.get_wishlist_by_game(game)

    return wishes

def check_if_user_has_wishlisted_game(user: User, game: Game, repo: WishlistRepository) -> bool:
    user_wishes = get_wishes_by_user(user, repo)

    for wish in user_wishes:
        if wish.game == game:
            return True

    return False


def wish_dto_to_wish(wish_dto: WishDTO, user_repository: ur.UserRepository, game_repository:gr.GameRepository, user=None, game=None):
    user = user if user is not None else user_service.get_user_by_username(wish_dto.username, user_repository)
    game = game if game is not None else game_service.get_game(wish_dto.game_id, game_repository)

    return Wish(user, game, wish_dto.wish_time)


from flask_wtf import FlaskForm
from wtforms import SubmitField

class WishlistForm(FlaskForm):
    #game_id = HiddenField("Game ID")
    submit_add = SubmitField("Add to wishlist")
    submit_remove = SubmitField("Remove from wishlist")