from flask import Blueprint, render_template, redirect, url_for

from games.authentication.authenticaton_blueprint import login_required
from games.service import review_service, game_service
from games.repository import review_repository, game_repository
from games.domainmodel.model import User, Review

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired

from games.utils import validation

from games.exceptions import view_layer_exceptions, service_layer_exceptions


review = Blueprint('review', __name__)

@review.route('/add', methods=['POST'])
@login_required
def add_review(authenticated_user: User):
    form = ReviewForm()
    if form.validate_on_submit():

        game_id = validation.validate_game_id(form.game_id.data)
        rating = validation.validate_rating(form.rating.data)
        comment = validation.validate_review_text(form.comment.data)

        print(comment)

        try:
            game = game_service.get_game(game_id, game_repository.game_repo_instance)
        except service_layer_exceptions.ResourceNotFoundException:
            raise view_layer_exceptions.NotFoundException(f"Game with game_id {game_id} does not exist")

        review = Review(
            authenticated_user,
            game,
            rating,
            comment
        )

        try:
            review_service.add_review(review, review_repository.review_repo_instance)
        except service_layer_exceptions.ResourceAlreadyExistsException:
            raise view_layer_exceptions.BadRequestException(f"Sorry, it looks like you already have a review for this game with the exact same comment, please leave a review with a new comment!")


        return redirect(url_for('games.game', game_id=game_id))
    else:
        raise view_layer_exceptions.BadRequestException("Invalid form submission, please make sure that you have filled in the comment correctly and are logged in!")



class ReviewForm(FlaskForm):
    game_id = HiddenField("Game ID", validators=[DataRequired()])
    rating = SelectField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')