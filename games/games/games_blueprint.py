from flask import Blueprint, request, current_app, render_template, session
from games.utils import validation, constants
from games.utils.rendering import render_template
from games.exceptions import view_layer_exceptions, service_layer_exceptions

from games.repository import game_repository, review_repository, user_repository, wishlist_repository
from games.service import game_service, review_service, user_service, wishlist_service
from games.domainmodel.model import User, Review, Game

from games.reviews.review_blueprint import ReviewForm


games = Blueprint('games', __name__)


@games.route('/')
def index(page_number=constants.DEFAULT_PAGE_NUMBER, count=constants.DEFAULT_COUNT, sort_by=constants.DEFAULT_SORT_BY, ascending=constants.DEFAULT_ASCENDING):

    page_number = validation.validate_page_number(request.args.get('page', page_number))
    count = validation.validate_count(request.args.get('count', count))
    sort_by = validation.validate_sort_by(request.args.get('sort_by', sort_by))
    ascending = validation.validate_ascending(request.args.get('ascending', ascending))

    if sort_by == 'default':
        page = game_service.get_games(repository=game_repository.game_repo_instance, page_number=page_number, count=count, reverse=ascending, endpoint='games.index', ascending=ascending)

    elif sort_by == 'title':
        page = game_service.get_games_sorted_alphabetically(repository=game_repository.game_repo_instance, page_number=page_number, count=count, reverse=ascending, endpoint='games.index', sort_by=sort_by, ascending=ascending)

    elif sort_by == 'release_date':
        page = game_service.get_games_sorted_by_date(repository=game_repository.game_repo_instance, page_number=page_number, count=count, reverse=(not ascending), endpoint='games.index', sort_by=sort_by, ascending=ascending)

    return render_template('browseGames.html', page=page)


@games.route('search')
def search(search_term:str="", page: int=constants.DEFAULT_PAGE_NUMBER, count: int=constants.DEFAULT_COUNT):
    search_term = validation.validate_search_term(request.args.get('q', search_term))
    page = validation.validate_page_number(request.args.get('page', page))
    count = validation.validate_count(request.args.get('count', count))

    page = game_service.search_games(search_term, repository=game_repository.game_repo_instance, page_number=page, count=count, reverse=False, endpoint='games.search', q=search_term)
    return render_template('browseGames.html', page=page)

from games.service.wishlist_service import WishlistForm

@games.route('game/<game_id>')
def game(game_id):
    game_id = validation.validate_game_id(game_id)

    try:
        game = game_service.get_game(game_id, game_repository=game_repository.game_repo_instance)
    except service_layer_exceptions.ResourceNotFoundException:
        raise view_layer_exceptions.NotFoundException(f"Game {game_id} not found")

    user = user_service.get_logged_in_user_from_session(session, user_repository.user_repo_instance)

    wishlisted_status = None

    if user is not None:
        wishlisted_status = wishlist_service.check_if_user_has_wishlisted_game(user, game, wishlist_repository.wishlist_repo_instance)

    # possible values for wishlisted_status: None/False/True
    # If None, the user is not logged in, don't display an add/remove from wishlist button

    form = WishlistForm()

    reviews = sorted(review_service.get_reviews_for_game(game, review_repository=review_repository.review_repo_instance), key=lambda review: review.rating, reverse=True)

    average_rating = None
    for review in reviews:
        if average_rating is None:
            average_rating = review.rating
        else:
            average_rating += review.rating

    if average_rating is not None:
        average_rating /= len(reviews)
        average_rating = round(average_rating, 1)


    return render_template('gameDescription.html', game=game, wishlist_form=form, wishlisted_status=wishlisted_status, reviews=reviews, review_form=ReviewForm(game_id=game.game_id), average_rating=average_rating)


@games.route('genre/<string:genre_name>')
def genre(genre_name: str, page=constants.DEFAULT_PAGE_NUMBER, count=constants.DEFAULT_COUNT):
    genre_name = validation.validate_genre_name(genre_name)
    page = validation.validate_page_number(request.args.get('page', page))
    count = validation.validate_count(request.args.get('count', count))

    try:
        genre = game_service.get_genre(genre_name, repository=game_repository.game_repo_instance)
    except service_layer_exceptions.ResourceNotFoundException:
        raise view_layer_exceptions.NotFoundException(f"Genre {genre_name} not found")

    page = game_service.get_games_with_genre(genre, repository=game_repository.game_repo_instance, page_number=page, count=count, reverse=False, endpoint='games.genre', genre_name=genre_name, ascending=False)

    return render_template('browseGamesGenre.html', page=page)

@games.route('publisher/<string:publisher_name>')
def publisher(publisher_name: str, page=constants.DEFAULT_PAGE_NUMBER, count=constants.DEFAULT_COUNT):
    publisher_name = validation.validate_publisher_name(publisher_name)
    page = validation.validate_page_number(request.args.get('page', page))
    count = validation.validate_count(request.args.get('count', count))

    try:
        publisher = game_service.get_publisher(publisher_name, repository=game_repository.game_repo_instance)
    except service_layer_exceptions.ResourceNotFoundException:
        raise view_layer_exceptions.NotFoundException(f"Publisher {publisher_name} not found")

    page = game_service.get_games_by_publisher(publisher, repository=game_repository.game_repo_instance, page_number=page, count=count, reverse=False, endpoint='games.publisher', publisher_name=publisher_name, ascending=False)

    return render_template('browseGamesPublisher.html', page=page)
