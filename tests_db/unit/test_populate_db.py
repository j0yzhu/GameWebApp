from games.repository.game_repository.adapters import database_game_repository
from games.repository.user_repository.adapters import database_user_repository
from games.repository.review_repository.adapters import database_review_repository
from games.repository.wishlist_repository.adapters import database_wishlist_repository

def test_population(session_context_manager):
    game_repository = database_game_repository.DatabaseGameRepository(session_context_manager)
    user_repository = database_user_repository.DatabaseUserRepository(session_context_manager)
    review_repository = database_review_repository.DatabaseReviewRepository(session_context_manager)
    wishlist_repository = database_wishlist_repository.DatabaseWishlistRepository(session_context_manager)

    game_repository.populate(True)
    user_repository.populate(True)
    review_repository.populate(True)
    wishlist_repository.populate(True)

    assert user_repository.get_number_of_users() != 0 # Assert that users have been added
    assert game_repository.get_number_of_games() != 0 # Assert that games have been added


    total = 0

    for user in user_repository.get_users(1, user_repository.get_number_of_users(), False):
        total += len(wishlist_repository.get_wishlist_by_user(user))

    assert total != 0

    total = 0

    for user in user_repository.get_users(1, user_repository.get_number_of_users(), False):
        total += len(review_repository.get_reviews_by_user(user))

    assert total != 0