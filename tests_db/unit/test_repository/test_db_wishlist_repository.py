import pytest

from games.repository.wishlist_repository.adapters import database_wishlist_repository
from games.repository.orm import SessionContextManager
from games.domainmodel.model import User, Game, Wish

from games.repository.game_repository.adapters import database_game_repository
from games.repository.user_repository.adapters import database_user_repository

from games.repository import wishlist_repository
from games.__init__ import create_app

from games.exceptions import repository_layer_exceptions

from games.config import Config

class TestDatabase:
    def test_population(self, populated_wishlist_repository):
        wishlist_repo = populated_wishlist_repository

        #check num users
        wishes = wishlist_repo.get_wishlist_by_user(User("joy", "password"))
        assert len(wishes) > 0

    def test_add_wish(self, unpopulated_wishlist_repository, unpopulated_game_repository, unpopulated_user_repository):
        wishlist_repo = unpopulated_wishlist_repository

        user = User("joy", "password")
        user2 = User("eli", "password")

        unpopulated_user_repository.add_user(user)
        unpopulated_user_repository.add_user(user2)

        game = Game(1, "Call of Duty")
        game2 = Game(2, "Call of Duty 2")

        unpopulated_game_repository.add_game(game)
        unpopulated_game_repository.add_game(game2)

        user = unpopulated_user_repository.get_user("joy")
        user2 = unpopulated_user_repository.get_user("eli")

        # adding new wish
        new_wish = Wish(user, game)
        wishlist_repo.add_wish(new_wish)

        # checking if wish is in populated data
        retrieved_wish = wishlist_repo.get_wishlist_by_user(user)
        assert retrieved_wish == [new_wish]

        # test for adding same wish again
        with pytest.raises(repository_layer_exceptions.ResourceAlreadyExistsException):
            wishlist_repo.add_wish(new_wish)

    def test_remove_wish(self, unpopulated_wishlist_repository, unpopulated_game_repository, unpopulated_user_repository):
        wishlist_repo = unpopulated_wishlist_repository

        user = User("joy", "password")
        user2 = User("eli", "password")

        unpopulated_user_repository.add_user(user)
        unpopulated_user_repository.add_user(user2)

        game = Game(1, "Call of Duty")
        game2 = Game(2, "Call of Duty 2")

        unpopulated_game_repository.add_game(game)
        unpopulated_game_repository.add_game(game2)

        user = unpopulated_user_repository.get_user("joy")
        user2 = unpopulated_user_repository.get_user("eli")

        # adding new wish
        new_wish = Wish(user, game)
        wishlist_repo.add_wish(new_wish)
        new_wish = wishlist_repo.get_wishlist_by_user(user)[0]

        # removing the wish
        wishlist_repo.remove_wish(new_wish)

        # checking if wish is in populated data
        retrieved_wish = wishlist_repo.get_wishlist_by_user(user)
        assert retrieved_wish == []

    def test_get_wishlist_by_user(self, unpopulated_wishlist_repository, unpopulated_game_repository, unpopulated_user_repository):
        wishlist_repo = unpopulated_wishlist_repository

        user = User("joy", "password")
        user2 = User("eli", "password")

        unpopulated_user_repository.add_user(user)
        unpopulated_user_repository.add_user(user2)

        game = Game(1, "Call of Duty")
        game2 = Game(2, "Call of Duty 2")

        unpopulated_game_repository.add_game(game)
        unpopulated_game_repository.add_game(game2)

        user = unpopulated_user_repository.get_user("joy")
        user2 = unpopulated_user_repository.get_user("eli")

        # is in populated data
        wishes = wishlist_repo.get_wishlist_by_user(user)
        assert wishes is not None
        assert len(wishes) == 0

        wishlist_repo.add_wish(Wish(user, game))
        wishlist_repo.add_wish(Wish(user, game2))
        wishlist_repo.add_wish(Wish(user2, game))

        wishes = wishlist_repo.get_wishlist_by_user(user)
        assert len(wishes) == 2