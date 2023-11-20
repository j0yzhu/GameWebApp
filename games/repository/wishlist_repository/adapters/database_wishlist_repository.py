from typing import List

from games.repository.wishlist_repository.wishlist_repository import WishlistRepository
from games.domainmodel.model import User, Game, Wish
from games.repository.wishlist_repository.adapters import csv_wishlist_repository

from games.exceptions import repository_layer_exceptions
from sqlalchemy.orm.exc import NoResultFound

from games.repository import game_repository, user_repository
from games.repository.user_repository.adapters import csv_user_repository
from games.repository.game_repository.adapters import csv_game_repository

class DatabaseWishlistRepository(WishlistRepository):
    def __init__(self, session_context_manager):
        self.__session_context_manager = session_context_manager

    def close_session(self):
        self.__session_context_manager.close_current_session()

    def reset_session(self):
        self.__session_context_manager.reset_session()

    def get_wishlist_by_user(self, user: User) -> List[Wish]:
        """
        Retrieves the wishlist for a specific user.
        :param user: the user object
        :return: list of games in the user's wishlist
        """
        with self.__session_context_manager as scm:
            user_wishlist = (
                scm.session.query(Wish)
                .join(User)
                .filter(User._User__username == user.username)
                .all()
            )
            return user_wishlist

    def get_wishlist_by_game(self, game: Game) -> List[Wish]:
        """
        Retrieves the wishlist for a specific user.
        :param user: the user object
        :return: list of games in the user's wishlist
        """
        with self.__session_context_manager as scm:
            game_wishlist = (
                scm.session.query(Wish)
                .join(User)
                .filter(Wish._Wish__game == game)
                .all()
            )
            return game_wishlist

    def get_wish(self, game: Game, user: User):
        with self.__session_context_manager as scm:
            try:
                wish = (
                    scm.session.query(Wish)
                    .join(User)
                    .filter(Wish._Wish__game == game)
                    .filter(Wish._Wish__user == user)
                    .one()
                )
                return wish
            except NoResultFound:
                raise repository_layer_exceptions.ResourceNotFoundException(
                    f"Wish for user {user.username} and game {game.title} does not exist"
                )

    def add_wish(self, wish: Wish):
        """
        Adds a game to a user's wishlist.
        :param user: the user object
        :param game: the game object
        """
        with self.__session_context_manager as scm:
            try:
                scm.session.expunge(wish)
            except: # If we can't expunge it, it already isn't in the session
                pass

        try:
            w = self.get_wish(wish.game, wish.user)
            print(w)
            raise repository_layer_exceptions.ResourceAlreadyExistsException(
                f"Wish for user {wish.user.username} and game {wish.game.title} already exists"
            )
        except repository_layer_exceptions.ResourceNotFoundException:
            pass

        with self.__session_context_manager as scm:
            scm.session.merge(wish)
            scm.commit()

    def remove_wish(self, wish: Wish):
        print(wish)
        with self.__session_context_manager as scm:
            scm.session.delete(wish)
            # print(scm.session.query(Wish).filter(Wish._Wish__game == wish.game).filter(Wish._Wish__user == wish.user).all())
            scm.commit()

    def populate(self, testing: bool=False):
        """
        Populates the repository with games
        """
        if not testing:
            return

        repo = csv_wishlist_repository.CSVWishlistRepository()
        repo.populate(testing)

        old_user_repo_instance = user_repository.user_repo_instance
        old_game_repo_instance = game_repository.game_repo_instance

        user_repo = csv_user_repository.CSVUserRepository()
        game_repo = csv_game_repository.CSVGameRepository()

        user_repo.populate(testing)
        game_repo.populate(testing)

        user_repository.user_repo_instance = user_repo
        game_repository.game_repo_instance = game_repo

        for user in user_repo.get_users(1, user_repo.get_number_of_users(), False):
            for wish in repo.get_wishlist_by_user(user):
                try:
                    with self.__session_context_manager as scm:

                        game = scm.session.query(Game).filter(Game._Game__game_id == wish.game.game_id).one()
                        user = scm.session.query(User).filter(User._User__username == wish.user.username).one()
                    wish._Wish__game = game

                    wish._Wish__user = user
                    self.add_wish(wish)
                except repository_layer_exceptions.ResourceAlreadyExistsException:
                    pass

        user_repository.user_repo_instance = old_user_repo_instance
        game_repository.game_repo_instance = old_game_repo_instance