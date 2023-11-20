import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from games.repository.orm import metadata, map_model_to_tables, SessionContextManager
from games.repository.game_repository.adapters import database_game_repository
from games.repository.review_repository.adapters import database_review_repository
from games.repository.user_repository.adapters import database_user_repository
from games.repository.wishlist_repository.adapters import database_wishlist_repository


TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///covid-19-test.db'

@pytest.fixture
def session_context_manager():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_context_manager = SessionContextManager(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    yield session_context_manager
    metadata.drop_all(engine)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)

@pytest.fixture
def unpopulated_game_repository(session_context_manager):
    game_repo = database_game_repository.DatabaseGameRepository(session_context_manager)
    return game_repo

@pytest.fixture
def populated_game_repository(session_context_manager):
    game_repo = database_game_repository.DatabaseGameRepository(session_context_manager)
    game_repo.populate(True)
    return game_repo

@pytest.fixture
def populated_user_repository(session_context_manager):
    user_repo = database_user_repository.DatabaseUserRepository(session_context_manager)
    user_repo.populate(True)
    return user_repo

@pytest.fixture
def unpopulated_user_repository(session_context_manager):
    user_repo = database_user_repository.DatabaseUserRepository(session_context_manager)
    return user_repo

@pytest.fixture
def populated_wishlist_repository(session_context_manager):
    user_repo = database_user_repository.DatabaseUserRepository(session_context_manager)
    user_repo.populate(True)
    game_repo = database_game_repository.DatabaseGameRepository(session_context_manager)
    game_repo.populate(True)
    wishlist_repo = database_wishlist_repository.DatabaseWishlistRepository(session_context_manager)
    wishlist_repo.populate(True)
    return wishlist_repo

@pytest.fixture
def unpopulated_wishlist_repository(session_context_manager):
    wishlist_repo = database_wishlist_repository.DatabaseWishlistRepository(session_context_manager)
    return wishlist_repo



@pytest.fixture
def unpopulated_review_repository(session_context_manager):
    review_repo = database_review_repository.DatabaseReviewRepository(session_context_manager)
    return review_repo

@pytest.fixture
def populated_review_repository(session_context_manager):
    review_repo = database_review_repository.DatabaseReviewRepository(session_context_manager)
    review_repo.populate(True)
    return review_repo