from games.utils.rendering import render_template
from flask import Blueprint

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('index.html')

@home.route('/attributions')
def attributions():
    return render_template('attributions.html')