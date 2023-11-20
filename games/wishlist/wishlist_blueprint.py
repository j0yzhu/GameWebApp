from games.utils.rendering import render_template
from games.authentication.authenticaton_blueprint import login_required
from games.domainmodel.model import Game, User, Wish
from games.service import game_service, wishlist_service
from games.repository import game_repository, wishlist_repository
from games.exceptions import service_layer_exceptions, view_layer_exceptions
from games.utils import validation
from flask import Blueprint, redirect, url_for

from games.service.wishlist_service import WishlistForm

wishlist = Blueprint('wishlist', __name__)

@wishlist.route('/add/<int:game_id>', methods=["POST"])
@login_required
def add(authenticated_user: User, game_id: int):
    form = WishlistForm()

    if not form.validate_on_submit():
        raise view_layer_exceptions.UnauthorizedException("Invalid or non-existent CSRF token")

    game_id = validation.validate_game_id(game_id)

    try:
        game = game_service.get_game(game_id, game_repository.game_repo_instance)
    except service_layer_exceptions.ResourceNotFoundException:
        raise view_layer_exceptions.NotFoundException(f"Game with game_id {game_id} does not exist")

    wish = Wish(authenticated_user, game)

    try:
        wishlist_service.add_wish(wish, wishlist_repository.wishlist_repo_instance)
    except service_layer_exceptions.ResourceAlreadyExistsException:
        raise view_layer_exceptions.BadRequestException(f"{str(game)} is already in your wishlist")

    return redirect(url_for('games.game', game_id=game_id))

@wishlist.route('/remove/<int:game_id>', methods=['POST'])
@login_required
def remove(authenticated_user: User, game_id: int):
    form = WishlistForm()

    if not form.validate_on_submit():
        raise view_layer_exceptions.UnauthorizedException("Invalid or non-existent CSRF token")


    game_id = validation.validate_game_id(game_id)

    try:
        game = game_service.get_game(game_id, game_repository.game_repo_instance)
    except service_layer_exceptions.ResourceNotFoundException:
        raise view_layer_exceptions.NotFoundException(f"Game with game_id {game_id} does not exist")

    actual_wish = None
    wishes = wishlist_service.get_wishes_by_user(authenticated_user, wishlist_repository.wishlist_repo_instance)
    for wish in wishes:
        if wish.game == game:
            actual_wish = wish
            break

    if actual_wish is None:
        raise view_layer_exceptions.BadRequestException(f"{str(game)} is not in your wishlist")




    try:
        wishlist_service.remove_wish(actual_wish, wishlist_repository.wishlist_repo_instance)
    except service_layer_exceptions.ResourceNotFoundException:
        raise view_layer_exceptions.BadRequestException(f"{str(game)} is not in your wishlist")

    return redirect(url_for('games.game', game_id=game_id))