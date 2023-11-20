import pytest

from games.utils import validation, constants
from games.exceptions.view_layer_exceptions import BadRequestException

raises_error = object()  # This is a unique object (sentinel) that we can use to signify that an error should be raised.

@pytest.mark.parametrize(
    "page_number,expected_result",
    [
        (1, 1),  # Assuming 1 is a valid page number
        (0, raises_error),  # Assuming 0 is not a valid page number
        (-1, raises_error),  # Negative numbers might not be valid either
        (None, raises_error),  # None is not a valid page number
        ("1", 1),  # Strings that can be converted to integers are valid
        ("0", raises_error),  # Strings that can be converted to integers are valid but they still need to be positive
        ("-1", raises_error),  # Strings that can be converted to integers are valid but they still need to be positive
        ("a", raises_error),  # Strings that cannot be converted to integers are not valid
        ("", raises_error),  # Empty strings are not valid
        (True, 1),  # Booleans are valid but they need to be converted to integers
        (False, raises_error),  # Booleans are valid but False == 0 so they still need to be positive
        (1.0, 1),  # Floats are valid but they need to be converted to integers
        (0.0, raises_error),  # Floats are valid but they need to be converted to integers
        (-1.0, raises_error),  # Floats are valid but they need to be converted to integers
        (1.1, 1),  # Floats are valid but they need to be converted to integers
    ]
)
def test_validate_page_number(page_number, expected_result):
    if expected_result is not raises_error:
        assert validation.validate_page_number(page_number) == expected_result
    else:
        with pytest.raises(BadRequestException):
            validation.validate_page_number(page_number)

@pytest.mark.parametrize(
    "count,expected_result",
    [
        (1, 1),  # Assuming 1 is a valid count
        (0, raises_error),  # Assuming 0 is not a valid count
        (-1, raises_error),  # Negative numbers might not be valid either
        (None, raises_error),  # None is not a valid count
        ("1", 1),  # Strings that can be converted to integers are valid
        ("0", raises_error),  # Strings that can be converted to integers are valid but they still need to be positive
        ("-1", raises_error),  # Strings that can be converted to integers are valid but they still need to be positive
        ("a", raises_error),  # Strings that cannot be converted to integers are not valid
        ("", raises_error),  # Empty strings are not valid
        (True, 1),  # Booleans are valid but they need to be converted to integers
        (False, raises_error),  # Booleans are valid but False == 0 so they still need to be positive
        (1.0, 1),  # Floats are valid but they need to be converted to integers
        (0.0, raises_error),  # Floats are valid but they need to be converted to integers
        (-1.0, raises_error),  # Floats are valid but they need to be converted to integers
        (1.1, 1),  # Floats are valid but they need to be converted to integers
        (constants.MAX_COUNT, constants.MAX_COUNT),  # Assuming MAX_COUNT is a valid count
        (constants.MAX_COUNT + 1, raises_error),  # Assuming MAX_COUNT + 1 is not a valid count
    ]
)

def test_validate_count(count, expected_result):
    if expected_result is not raises_error:
        assert validation.validate_count(count) == expected_result
    else:
        with pytest.raises(BadRequestException):
            validation.validate_count(count)

@pytest.mark.parametrize(
    "search_term,expected_result",
    [
        ("gta", "gta"),  # Assuming "gta" is a valid search term
        ("", raises_error),  # Assuming "" is not a valid search term
        (None, raises_error),  # Assuming None is not a valid search term
        (True, raises_error),  # Assuming True is not a valid search term
        (False, raises_error),  # Assuming False is not a valid search term
        (1, raises_error),  # Assuming 1 is not a valid search term
        (1.0, raises_error),  # Assuming 1.0 is not a valid search term
        ("   ", raises_error) # Assuming "   " is not a valid search term
    ]
)
def test_validate_search_term(search_term, expected_result):
    if expected_result is not raises_error:
        assert validation.validate_search_term(search_term) == expected_result
    else:
        with pytest.raises(BadRequestException):
            validation.validate_search_term(search_term)

@pytest.mark.parametrize(
    "game_id,expected_result",
    [
        (1, 1),  # Assuming 1 is a valid page number
        (0, raises_error),  # Assuming 0 is not a valid page number
        (-1, raises_error),  # Negative numbers might not be valid either
        (None, raises_error),  # None is not a valid page number
        ("1", 1),  # Strings that can be converted to integers are valid
        ("0", raises_error),  # Strings that can be converted to integers are valid but they still need to be positive
        ("-1", raises_error),  # Strings that can be converted to integers are valid but they still need to be positive
        ("a", raises_error),  # Strings that cannot be converted to integers are not valid
        ("", raises_error),  # Empty strings are not valid
        (True, 1),  # Booleans are valid but they need to be converted to integers
        (False, raises_error),  # Booleans are valid but False == 0 so they still need to be positive
        (1.0, 1),  # Floats are valid but they need to be converted to integers
        (0.0, raises_error),  # Floats are valid but they need to be converted to integers
        (-1.0, raises_error),  # Floats are valid but they need to be converted to integers
        (1.1, 1),  # Floats are valid but they need to be converted to integers
    ]
)

def test_validate_game_id(game_id, expected_result):
    if expected_result is not raises_error:
        assert validation.validate_game_id(game_id) == expected_result
    else:
        with pytest.raises(BadRequestException):
            validation.validate_game_id(game_id)

@pytest.mark.parametrize(
    "genre_name,expected_result",
    [
        ("gta", "gta"),  # Assuming "gta" is a valid search term
        ("", raises_error),  # Assuming "" is not a valid search term
        (None, raises_error),  # Assuming None is not a valid search term
        (True, raises_error),  # Assuming True is not a valid search term
        (False, raises_error),  # Assuming False is not a valid search term
        (1, raises_error),  # Assuming 1 is not a valid search term
        (1.0, raises_error),  # Assuming 1.0 is not a valid search term
        ("   ", raises_error) # Assuming "   " is not a valid search term
    ]
)
def test_validate_genre_name(genre_name, expected_result):
    if expected_result is not raises_error:
        assert validation.validate_genre_name(genre_name) == expected_result
    else:
        with pytest.raises(BadRequestException):
            validation.validate_genre_name(genre_name)

@pytest.mark.parametrize(
    "publisher_name,expected_result",
    [
        ("gta", "gta"),  # Assuming "gta" is a valid search term
        ("", raises_error),  # Assuming "" is not a valid search term
        (None, raises_error),  # Assuming None is not a valid search term
        (True, raises_error),  # Assuming True is not a valid search term
        (False, raises_error),  # Assuming False is not a valid search term
        (1, raises_error),  # Assuming 1 is not a valid search term
        (1.0, raises_error),  # Assuming 1.0 is not a valid search term
        ("   ", raises_error) # Assuming "   " is not a valid search term
    ]
)
def test_validate_publisher_name(publisher_name, expected_result):
    if expected_result is not raises_error:
        assert validation.validate_publisher_name(publisher_name) == expected_result
    else:
        with pytest.raises(BadRequestException):
            validation.validate_publisher_name(publisher_name)