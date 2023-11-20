from functools import wraps
from flask import redirect, session, url_for, Blueprint, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo

from password_validator import PasswordValidator
import games.service.user_service as user_service
from games.repository import user_repository

from games.exceptions import service_layer_exceptions, view_layer_exceptions


authentication = Blueprint('authentication', __name__)

""""@authentication.route('/login', methods=['POST'])
def login_form():#Assuming Login Form is registering the account
    '''
    Login page for the application.
    '''
"""
@authentication.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Login page for the application.
    '''
    form = RegistrationForm()
    error_message = None
    status_code = 200
    if form.validate_on_submit():
        try:
            user_service.add_user(form.user_name.data, form.password.data, user_repository.user_repo_instance)
            session['username'] = form.user_name.data
            return redirect(url_for('home.index'))
        except service_layer_exceptions.ResourceAlreadyExistsException:
            error_message = 'Username already taken.'
            status_code = 409  # 409 is the status code for conflict, which is what we return if the username is already taken

    session.pop('username', None)
    return render_template('register.html', form=form, error_message=error_message), status_code


@authentication.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login page for the application.
    '''

    form = LoginForm()
    error_message = None
    status_code = 200
    if form.validate_on_submit():
        try:
            user = user_service.authenticate_user(form.user_name.data, form.password.data, user_repository.user_repo_instance)
            session['username'] = user.username
            return redirect(url_for('home.index'))
        except service_layer_exceptions.AuthenticationException:
            error_message = 'Incorrect username or password.'
            status_code = 401
    return render_template('login.html', form=form, error_message=error_message), status_code


@authentication.route('/logout', methods=['GET'])
def logout():
    '''
    Logs the user out by removing the user_name from the session.
    '''

    if session.get('username'):
        session.pop('username', None) # Remove the user_name from the session
        return redirect(url_for('home.index'))
    else:
        raise view_layer_exceptions.UnauthorizedException("You must be logged in to log out.")  # If the user is not logged in, we raise an exception (returns 401)

def login_required(view):
    '''
    Decorator that redirects anonymous users to the login page if they try to visit a page that requires authentication and they are not logged in.
    '''
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication.login'))

        try:
            authenticated_user = user_service.get_user_by_username(session['username'], user_repository.user_repo_instance)  # When login is required, we fetch the user object from the database.
        except service_layer_exceptions.ResourceNotFoundException:
            session.pop('username') # remove the invalid username from the session
            return redirect(url_for('authentication.login')) # If the account doesn't exist, redirect them to the login page
        # Since the session is signed, the only way a valid user_name can be in the session object is if it was signed by the application.

        return view(authenticated_user, **kwargs) # We pass the user object to the view function
    return wrapped_view


#need this function to validate passwords for registering and logging in
def validate_password(form, field):
    password = field.data
    schema = PasswordValidator()
    schema \
        .min(6) \
        .has().uppercase() \
        .has().digits()
    # Validate the password using the schema
    if not schema.validate(password):
        raise ValidationError(
            "Password must be at least 6 characters long, contain at least one uppercase letter, and one digit.")

class RegistrationForm(FlaskForm):
    user_name = StringField("Username", [DataRequired(), Length(min=3)])
    password = PasswordField("Password", [DataRequired(), validate_password])
    confirm_password = PasswordField('Confirm Password', [DataRequired(), Length(min=6),
                                                     EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_name = StringField("Username", [DataRequired(), Length(min=3)])
    password = PasswordField("Password", [DataRequired()]) #  We shouldn't require specific password criteria for logging in, incase the criteria changes in the future a user could be locked out of their account
    submit = SubmitField('Login')