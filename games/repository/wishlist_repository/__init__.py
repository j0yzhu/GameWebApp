from games.repository.wishlist_repository.wishlist_repository import WishlistRepository
from games.repository.wishlist_repository.adapters import csv_wishlist_repository

def create(adapter_type, testing: bool=None) -> WishlistRepository:
    if adapter_type == "csv":
        c = csv_wishlist_repository.CSVWishlistRepository()

    elif adapter_type == "database":
        c = database_wishlist_repository.DatabaseWishlistRepository()

    c.populate(testing)
    return c

wishlist_repo_instance: WishlistRepository = None
