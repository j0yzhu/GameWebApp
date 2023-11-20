from games.utils.rendering import render_template
from flask import Blueprint
from games.authentication.authenticaton_blueprint import login_required
from games.domainmodel.model import User, Review, Game

from games.repository import user_repository, review_repository, wishlist_repository, game_repository
from games.service import wishlist_service
from games.service import game_service

from games.service import user_service
from games.service import review_service

from games.exceptions import service_layer_exceptions, view_layer_exceptions

profile = Blueprint('profile', __name__)

# /profile goes to the current user
@profile.route('/')
@login_required
def logged_in_user_profile(authenticated_user: User):
    user = authenticated_user
    reviews = review_service.get_reviews_by_user(user, review_repository.review_repo_instance)
    wishlist = wishlist_service.get_wishes_by_user(user, wishlist_repository.wishlist_repo_instance)


    return render_template('profilePage.html', user=user, reviews=reviews, wishlist=wishlist)

# /profile/username goes to specific user
@profile.route('/<string:username>')
@login_required
def profile_for_username(authenticated_user: User, username: str):
    try:
        user = user_service.get_user_by_username(username, user_repository.user_repo_instance)
    except service_layer_exceptions.ResourceNotFoundException:
        raise view_layer_exceptions.NotFoundException(f"User with username {username} does not exist")

    reviews = review_service.get_reviews_by_user(user, review_repository.review_repo_instance)
    wishlist = wishlist_service.get_wishes_by_user(user, wishlist_repository.wishlist_repo_instance)

    return render_template('profilePage.html', user=user, reviews=reviews, wishlist=wishlist)