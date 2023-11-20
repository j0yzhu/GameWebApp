from games.exceptions import view_layer_exceptions
from games.utils import constants

def validate_page_number(page_number):
    if page_number is None:
        raise view_layer_exceptions.BadRequestException("No page number provided.")
    try:
        page_number = int(page_number)
    except ValueError:
        raise view_layer_exceptions.BadRequestException("Page number must be an integer.")
    if page_number < 1:
        raise view_layer_exceptions.BadRequestException("Page number must be a positive integer.")
    return page_number

def validate_count(count):
    if count is None:
        raise view_layer_exceptions.BadRequestException("No count provided.")
    try:
        count = int(count)
    except ValueError:
        raise view_layer_exceptions.BadRequestException("Count must be an integer.")
    if count < 1:
        raise view_layer_exceptions.BadRequestException("Count must be a positive integer.")
    if count > constants.MAX_COUNT:
        raise view_layer_exceptions.BadRequestException(f"Count must be less than or equal to {constants.MAX_COUNT}.")
    return count

def validate_search_term(search_term):
    if search_term is None:
        raise view_layer_exceptions.BadRequestException("No search term provided.")
    if not isinstance(search_term, str):
        raise view_layer_exceptions.BadRequestException("Search term must be a string.")
    if len(search_term.strip()) < 1:
        raise view_layer_exceptions.BadRequestException("Search term must be at least 1 character long.")
    return search_term.strip()

def validate_game_id(game_id):
    if game_id is None:
        raise view_layer_exceptions.BadRequestException("No game id provided.")
    try:
        game_id = int(game_id)
    except ValueError:
        raise view_layer_exceptions.BadRequestException("Game id must be an integer.")
    if game_id < 1:
        raise view_layer_exceptions.BadRequestException("Game id must be a positive integer.")
    return game_id

def validate_rating(rating):
    if rating is None:
        raise view_layer_exceptions.BadRequestException("No rating provided.")
    try:
        rating = int(rating)
    except ValueError:
        raise view_layer_exceptions.BadRequestException("rating must be an integer.")
    if rating < 0 or rating > 5:
        raise view_layer_exceptions.BadRequestException("Rating must be a nonnegative integer. 0 <= rating <= 5")
    return rating


def validate_genre_name(genre_name):
    if genre_name is None:
        raise view_layer_exceptions.BadRequestException("No genre name provided.")
    if not isinstance(genre_name, str):
        raise view_layer_exceptions.BadRequestException("Genre name must be a string.")
    if len(genre_name.strip()) < 1:
        raise view_layer_exceptions.BadRequestException("Genre name must be at least 1 character long.")
    return genre_name.strip()

def validate_publisher_name(publisher_name):
    if publisher_name is None:
        raise view_layer_exceptions.BadRequestException("No publisher name provided.")
    if not isinstance(publisher_name, str):
        raise view_layer_exceptions.BadRequestException("Publisher name must be a string.")
    if len(publisher_name.strip()) < 1:
        raise view_layer_exceptions.BadRequestException("Publisher name must be at least 1 character long.")
    return publisher_name.strip()

def validate_sort_by(sort_by):
    if sort_by is None:
        raise view_layer_exceptions.BadRequestException("No sort by provided.")
    if not isinstance(sort_by, str):
        raise view_layer_exceptions.BadRequestException("Sort by must be a string.")
    if sort_by not in constants.SORT_BY_OPTIONS:
        raise view_layer_exceptions.BadRequestException(f"Sort by must be one of {constants.SORT_BY_OPTIONS}.")
    return sort_by

def validate_ascending(ascending):
    if ascending is None:
        return ascending
    if not isinstance(ascending, bool):
        if isinstance(ascending, str):
            if ascending.lower() == 'true':
                return True
            elif ascending.lower() == 'false':
                return False
            # else fall through to exception
        raise view_layer_exceptions.BadRequestException("Ascending must be a boolean.")
    return ascending


def validate_review_text(review_text):
    if review_text is None:
        raise view_layer_exceptions.BadRequestException("No review text provided.")
    if not isinstance(review_text, str):
        raise view_layer_exceptions.BadRequestException("Review text must be a string.")
    if len(review_text.strip()) < 1:
        raise view_layer_exceptions.BadRequestException("Review text must be at least 1 character long.")
    if len(review_text.strip()) > 300:
        raise view_layer_exceptions.BadRequestException(f"Review text must be less than or equal to 300 characters long.")
    return review_text.strip()