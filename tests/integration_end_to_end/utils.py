import pytest
from games.__init__ import create_app
from flask import session

from games.config import Config

config = Config()

config.TESTING = True
config.REPOSITORY_ADAPTER_TYPE = "database"
config.WTF_CSRF_ENABLED = False
config.SECRET_KEY = "test"

@pytest.fixture()
def client():
    my_app = create_app(custom_config=config)

    return my_app.test_client()