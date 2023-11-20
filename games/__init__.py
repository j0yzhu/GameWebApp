"""Initialize Flask app."""
from flask import Flask

from games.repository import game_repository, user_repository, review_repository, wishlist_repository

from games.exceptions.base_exceptions import AbstractRequestException, ServiceLayerException, RepositoryLayerException
from games.games import games_blueprint
from games.home import home_blueprint
from games.authentication import authenticaton_blueprint
from games.wishlist import wishlist_blueprint
from games.profile import profile_blueprint
from games.utils.rendering import render_template # custom render_template that automatically passes in genres to create sidebar
from games.config import Config
from games.reviews import review_blueprint

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool
from games.repository.orm import metadata, map_model_to_tables

from games.repository.game_repository.adapters import csv_game_repository, database_game_repository
from games.repository.user_repository.adapters import csv_user_repository, database_user_repository
from games.repository.review_repository.adapters import csv_review_repository, database_review_repository
from games.repository.wishlist_repository.adapters import csv_wishlist_repository, database_wishlist_repository

from games.repository.orm import SessionContextManager

def create_app(custom_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)


    if custom_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_object(custom_config)


    testing = app.config.get('TESTING')

    print(testing)

    repository_adapter_type = app.config.get('REPOSITORY_ADAPTER_TYPE')

    if repository_adapter_type == 'database':
        database_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        if testing:
            database_uri = database_uri + "_test"
        database_echo = app.config.get('SQLALCHEMY_ECHO')

        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool, echo=database_echo)

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        session_context = SessionContextManager(session_factory)

        game_repository.game_repo_instance = database_game_repository.DatabaseGameRepository(session_context)
        user_repository.user_repo_instance = database_user_repository.DatabaseUserRepository(session_context)
        review_repository.review_repo_instance = database_review_repository.DatabaseReviewRepository(session_context)
        wishlist_repository.wishlist_repo_instance = database_wishlist_repository.DatabaseWishlistRepository(session_context)

        if app.config['TESTING'] is True or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            game_repository.game_repo_instance.populate(testing)
            user_repository.user_repo_instance.populate(testing)
            review_repository.review_repo_instance.populate(testing)
            wishlist_repository.wishlist_repo_instance.populate(testing)

            print("REPOPULATING DATABASE... FINISHED")
        else:
            map_model_to_tables()


    elif repository_adapter_type == 'csv':
        game_repository.game_repo_instance = csv_game_repository.CSVGameRepository()
        user_repository.user_repo_instance = csv_user_repository.CSVUserRepository()
        review_repository.review_repo_instance = csv_review_repository.CSVReviewRepository()
        wishlist_repository.wishlist_repo_instance = csv_wishlist_repository.CSVWishlistRepository()

        game_repository.game_repo_instance.populate(testing)
        user_repository.user_repo_instance.populate(testing)
        review_repository.review_repo_instance.populate(testing)
        wishlist_repository.wishlist_repo_instance.populate(testing)



    app.register_blueprint(home_blueprint.home)
    app.register_blueprint(games_blueprint.games, url_prefix='/games')
    app.register_blueprint(authenticaton_blueprint.authentication, url_prefix='/authentication')
    app.register_blueprint(wishlist_blueprint.wishlist, url_prefix='/wishlist')
    app.register_blueprint(profile_blueprint.profile, url_prefix='/profile')
    app.register_blueprint(review_blueprint.review, url_prefix='/review')
    @app.errorhandler(AbstractRequestException)
    def handle_request_exception(error):
        return render_template('error.html', error=error), error.status_code

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()