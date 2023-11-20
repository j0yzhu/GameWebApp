"""Flask configuration variables."""
from os import environ
from dotenv import load_dotenv

# Load environment variables from file .env, stored in this directory.
load_dotenv()

class Config:
    """Set Flask configuration from .env file."""

    # Flask configuration
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SECRET_KEY = environ.get('SECRET_KEY')

    TESTING = environ.get('TESTING')=="True"

    # Repository configuration
    REPOSITORY_ADAPTER_TYPE = environ.get('REPOSITORY_ADAPTER_TYPE')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = environ.get('SQLALCHEMY_ECHO')=="True"
    WTF_CSRF_ENABLED = environ.get('WTF_CSRF_ENABLED')=="True"