import csv
from pathlib import Path
from typing import List
from games.repository.wishlist_repository.wishlist_repository import WishDTO, WishlistRepository

from games.domainmodel.model import User, Game, Wish

from games.exceptions.repository_layer_exceptions import ResourceAlreadyExistsException, ResourceNotFoundException
from datetime import datetime

from games.service.wishlist_service import wish_dto_to_wish
from games.repository import user_repository, game_repository

class CSVWishlistRepository(WishlistRepository):

    def __init__(self):
        self.__dataset_of_wishlists = set()

    def get_wishlist_by_user(self, user: User) -> List[Wish]:
        sorted_wishes = sorted([wish for wish in self.__dataset_of_wishlists if wish.username == user.username], key=lambda x:x.wish_time)
        return [wish_dto_to_wish(wish, user_repository.user_repo_instance, game_repository.game_repo_instance, user=user) for wish in sorted_wishes]

    def get_wishlist_by_game(self, game: Game) -> List[Wish]:
        sorted_wishes = sorted([wish for wish in self.__dataset_of_wishlists if wish.game_id == game.game_id], key=lambda x:x.wish_time)
        return [wish_dto_to_wish(wish, user_repository.user_repo_instance, game_repository.game_repo_instance, game=game) for wish in sorted_wishes]

    def add_wish(self, wish: Wish):
        wish_dto = WishDTO(
            wish.user.username,
            wish.game.game_id,
            wish.wish_time
        )

        if wish_dto in self.__dataset_of_wishlists:
            raise ResourceAlreadyExistsException(
                f'Wish with user <{wish_dto.username}> and game_id <{wish_dto.game_id}> already exists')

        self.__dataset_of_wishlists.add(wish_dto)

    def remove_wish(self, wish: Wish):
        wish_dto = WishDTO(
            wish.user.username,
            wish.game.game_id,
            wish.wish_time
        )

        if wish_dto not in self.__dataset_of_wishlists:
            raise ResourceNotFoundException(f'Wishlist with user <{wish_dto.username}> and game_id <{wish_dto.game_id}> does not exist.')

        self.__dataset_of_wishlists.remove(wish_dto)

    def __read_csv_file(self, testing):
        if testing:
            path = Path(__file__).parent.parent / "data" / "test_wishlist.csv"
        else:
            path = Path(__file__).parent.parent / "data" / "wishlist.csv"

        with open(path, mode='r', encoding='utf-8-sig') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                wishlist = WishDTO(
                    row['username'],
                    int(row['game_id']),
                    (row.get('wish_time') or datetime.now())
                )

                self.__dataset_of_wishlists.add(wishlist)

    def populate(self, testing=False):
        self.__read_csv_file(testing)