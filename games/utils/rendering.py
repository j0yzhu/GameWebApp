from flask import render_template as flask_render_template
from flask import current_app

from games.service import game_service
from games.repository import game_repository

def render_template(template_name, **kwargs):
    """Render template with some default values."""
    return flask_render_template(template_name, genres=game_service.get_genres(game_repository.game_repo_instance), **kwargs)