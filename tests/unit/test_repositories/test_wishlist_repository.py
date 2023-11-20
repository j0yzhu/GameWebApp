import pytest
from games.domainmodel.model import Wish, User, Game
from games.repository.wishlist_repository.wishlist_repository import WishDTO
from games.repository.wishlist_repository.adapters import csv_wishlist_repository
from games.exceptions.repository_layer_exceptions import ResourceAlreadyExistsException, ResourceNotFoundException
from datetime import datetime

from games.repository import user_repository, game_repository

class TestCSVReader:
    @pytest.fixture()
    def unpopulated_wishlist_repository(self):
        user_repository.user_repo_instance = user_repository.csv_user_repository.CSVUserRepository()
        game_repository.game_repo_instance = game_repository.csv_game_repository.CSVGameRepository()
        return csv_wishlist_repository.CSVWishlistRepository()

    @pytest.fixture()
    def populated_wishlist_repository(self):
        user_repository.user_repo_instance = user_repository.csv_user_repository.CSVUserRepository()
        game_repository.game_repo_instance = game_repository.csv_game_repository.CSVGameRepository()
        repo = csv_wishlist_repository.CSVWishlistRepository()
        repo.populate(True)
        return repo


    def test_population(self, populated_wishlist_repository):
        """
        Test if when we populate from CSV, there is some data
        """

        u1 = User('max', 'password')  # make some users
        u2 = User('eli', 'password')
        u3 = User('joy', 'pawssword')
        user_repository.user_repo_instance.add_user(u1)  # add them to the user test_repository
        user_repository.user_repo_instance.add_user(u2)
        user_repository.user_repo_instance.add_user(u3)

        game1 = Game(7940, "blah")  # make some games
        game2 = Game(1228870, "blah")
        game3 = Game(311120, "blah")
        game4 = Game(410320, "blah")
        game_repository.game_repo_instance.add_game(game1)  # add them to the game test_repository
        game_repository.game_repo_instance.add_game(game2)
        game_repository.game_repo_instance.add_game(game3)
        game_repository.game_repo_instance.add_game(game4)

        # use get_review_by_user
        wishlist_1 = populated_wishlist_repository.get_wishlist_by_user(u1)  # get wishlists for each user
        wishlist_2 = populated_wishlist_repository.get_wishlist_by_user(u2)
        wishlist_3 = populated_wishlist_repository.get_wishlist_by_user(u3)
        # assert that the reviews we retrieve match the ones in test_wishlists.csv


        #sorting the wishlists, if you don't theres errors with the checks
        wishlist_1 = sorted(wishlist_1, key=lambda x: (x.user.username, x.game.game_id))
        wishlist_2 = sorted(wishlist_2, key=lambda x: (x.user.username, x.game.game_id))
        wishlist_3 = sorted(wishlist_3, key=lambda x: (x.user.username, x.game.game_id))

        assert wishlist_1[0].user.username == 'max'
        assert wishlist_1[0].game.game_id == 7940

        assert wishlist_1[1].user.username == 'max'
        assert wishlist_1[1].game.game_id == 1228870

        assert wishlist_2[0].user.username == 'eli'
        assert wishlist_2[0].game.game_id == 311120

        assert wishlist_3[0].user.username == 'joy'
        assert wishlist_3[0].game.game_id == 410320


    def test_empty_wishlist_csv(self, unpopulated_wishlist_repository):
        # The CSV file is empty, so wishlists should be empty for all users and games.
        u1 = User('max', 'password')
        game1 = Game(1, 'Game 1')

        wishlist_u1 = unpopulated_wishlist_repository.get_wishlist_by_user(u1)
        wishlist_game1 = unpopulated_wishlist_repository.get_wishlist_by_game(game1)

        assert not wishlist_u1
        assert not wishlist_game1

    def test_add_and_remove_wishlist_items(self, unpopulated_wishlist_repository):

        game1 = Game(1, 'Game 1')
        game2 = Game(2, 'Game 2')

        game_repository.game_repo_instance.add_game(game1)
        game_repository.game_repo_instance.add_game(game2)

        # Create a User object
        user = User('max', 'password')

        user_repository.user_repo_instance.add_user(user)


        # Add items to the wishlist

        w1 = Wish(user, game1)
        w2 = Wish(user, game2)
        unpopulated_wishlist_repository.add_wish(w1)
        unpopulated_wishlist_repository.add_wish(w2)


        # Check if they are in the wishlist
        wishlist_u1 = unpopulated_wishlist_repository.get_wishlist_by_user(user)
        assert Wish(user, game1) in wishlist_u1
        assert Wish(user, game2) in wishlist_u1
        # Remove an item and check if it's removed
        unpopulated_wishlist_repository.remove_wish(w1)

        wishlist_u1 = unpopulated_wishlist_repository.get_wishlist_by_user(user)
        assert Wish(user, game1) not in wishlist_u1
        assert Wish(user, game2) in wishlist_u1

    def test_adding_duplicate_games(self, unpopulated_wishlist_repository):
        # Create a User object and a Game object
        user = User('max', 'password')
        game1 = Game(1, 'Game 1')
        user_repository.user_repo_instance.add_user(user)
        game_repository.game_repo_instance.add_game(game1)

        # Add the same game to the wishlist twice

        w1 = Wish(user, game1)
        unpopulated_wishlist_repository.add_wish(w1)

        # Use a context manager to capture the exception
        with pytest.raises(ResourceAlreadyExistsException):
            unpopulated_wishlist_repository.add_wish(w1)

        # Ensure that there is only one game wishlisted
        wishlist_u1 = unpopulated_wishlist_repository.get_wishlist_by_user(user)
        assert len(wishlist_u1) == 1


    def test_removing_game_not_in_wishlist(self, unpopulated_wishlist_repository):
        user = User('max', 'password')
        game1 = Game(1, 'Game 1')
        game2 = Game(2, 'Game 2')

        user_repository.user_repo_instance.add_user(user)
        game_repository.game_repo_instance.add_game(game1)
        game_repository.game_repo_instance.add_game(game2)

        w1 = Wish(user, game1)
        w2 = Wish(user, game2)

        # Add the game 1 to the wishlist
        unpopulated_wishlist_repository.add_wish(w1)

        # Remove the game 2 from the wishlist
        with pytest.raises(ResourceNotFoundException):
            unpopulated_wishlist_repository.remove_wish(w2)

        wishlist_u1 = unpopulated_wishlist_repository.get_wishlist_by_user(user)

        # Check if length of wishlist is still 1
        assert len(wishlist_u1) == 1