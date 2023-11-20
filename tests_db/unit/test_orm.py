import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import Game, Genre, User, Review, Publisher, Wish

from sqlalchemy.exc import IntegrityError

def insert_user(empty_session, user: User):
    empty_session.execute(
            'INSERT INTO users (username, password) VALUES (:username, :password)',
            {'username': user.username, 'password': user.password}
        )

    row = empty_session.execute(
            'SELECT id FROM users WHERE username=:username',
            {'username': user.username}
        ).fetchone()

    return row


def insert_game(empty_session, game: Game) -> [Game]:
    empty_session.execute(
            'INSERT INTO games (id, title, publisher_name, price, release_date, description, image_url, website_url) VALUES (:id, :title, :publisher_name, :price, :release_date, :description, :image_url, :website_url)',
            {'id': game.game_id, 'title': game.title, 'publisher_name': game.publisher, 'price': game.price, 'release_date': game.release_date, 'description': game.description, 'image_url': game.image_url, 'website_url': game.website_url}
        )

    row = empty_session.execute(
        'SELECT id FROM games WHERE title=:title',
        {'title': game.title}
    ).fetchone()

    return row

def insert_genre(empty_session, genre: Genre) -> [Genre]:
    empty_session.execute(
            'INSERT INTO genres (name) VALUES (:name)',
            {'name': genre.genre_name}
        )

    row = empty_session.execute(
        'SELECT name FROM genres WHERE name=:name',
        {'name': genre.genre_name}
    ).fetchone()

    return row


def insert_genre_game_relationship(empty_session, game: Game, genre: Genre):
    empty_session.execute(
            'INSERT INTO game_genre_relationship (game_id, genre_name) VALUES (:game_id, :genre_name)',
            {'game_id': game.game_id, 'genre_name': genre.genre_name}
        )

    row = empty_session.execute(
        'SELECT game_id, genre_name FROM game_genre_relationship WHERE game_id=:game_id AND genre_name=:genre_name',
        {'game_id': game.game_id, 'genre_name': genre.genre_name}
    ).fetchone()

    return row


def insert_publisher(empty_session, publisher: Publisher) -> [Publisher]:
    empty_session.execute(
            'INSERT INTO publishers (name) VALUES (:name)',
            {'name': publisher.publisher_name}
        )

    row = empty_session.execute(
        'SELECT name FROM publishers WHERE name=:name',
        {'name': publisher.publisher_name}
    ).fetchone()

    return row

def insert_review(empty_session, review: Review) -> [Review]:
    user_id = empty_session.execute(
        'SELECT id FROM users WHERE username=:username',
        {'username': review.user.username}
    ).fetchone()[0]

    empty_session.execute(
            'INSERT INTO reviews (user_id, game_id, rating, comment) VALUES (:user_id, :game_id, :rating, :comment)',
            {'user_id': user_id, 'game_id': review.game.game_id, 'rating': review.rating, 'comment': review.comment}
        )

    row = empty_session.execute(
        'SELECT user_id, game_id, rating, comment FROM reviews WHERE user_id=:user_id AND game_id=:game_id AND rating=:rating AND comment=:comment',
        {'user_id': review.user_id, 'game_id': review.game_id, 'rating': review.rating, 'comment': review.comment}
    ).fetchone()

    return row

def insert_wish(empty_session, wish: Wish) -> [Wish]:
    user_id = empty_session.execute(
        'SELECT id FROM users WHERE username=:username',
        {'username': wish.user.username}
    ).fetchone()[0]

    empty_session.execute(
            'INSERT INTO wish (user_id, game_id, date_added) VALUES (:user_id, :game_id, :date_added)',
            {'user_id': user_id, 'game_id': wish.game.game_id, 'date_added': wish.wish_time}
        )

    row = empty_session.execute(
        'SELECT user_id, game_id, date_added FROM wish WHERE user_id=:user_id AND game_id=:game_id AND date_added=:date_added',
        {'user_id': user_id, 'game_id': wish.game.game_id, 'date_added': wish.wish_time}
    ).fetchone()

    return row


def test_add_retrieve_users(empty_session):
    user = User('Martin', '123456789')
    user2 = User('Martin2', '123456789')

    insert_user(empty_session, user)
    insert_user(empty_session, user2)

    expected = [user, user2]

    assert sorted(expected) == sorted(empty_session.query(User).all())  # make sure all the users were added

    with pytest.raises(IntegrityError):
        insert_user(empty_session, user) # Try adding a user with the same username

def test_add_retrieve_games(empty_session):
    game = Game(1, 'Cool game')
    game2 = Game(2, 'Cool game2')

    insert_game(empty_session, game)
    insert_game(empty_session, game2)

    expected = [game, game2]

    assert sorted(expected) == sorted(empty_session.query(Game).all())  # make sure all the games were added

    with pytest.raises(IntegrityError):
        insert_game(empty_session, game) # Try adding a game with the same id


def test_add_retrieve_genres(empty_session):
    genre = Genre('Cool genre')
    genre2 = Genre('Cool genre2')

    insert_genre(empty_session, genre)
    insert_genre(empty_session, genre2)

    expected = [genre, genre2]

    assert sorted(expected) == sorted(empty_session.query(Genre).all())  # make sure all the genres were added

    with pytest.raises(IntegrityError):
        insert_genre(empty_session, genre) # Try adding a genre with the same name

def test_add_retrieve_publishers(empty_session):
    publisher = Publisher('Cool publisher')
    publisher2 = Publisher('Cool publisher2')

    insert_publisher(empty_session, publisher)
    insert_publisher(empty_session, publisher2)

    expected = [publisher, publisher2]

    assert sorted(expected) == sorted(empty_session.query(Publisher).all())  # make sure all the publishers were added

    with pytest.raises(IntegrityError):
        insert_publisher(empty_session, publisher) # Try adding a publisher with the same name

def test_add_retrieve_reviews(empty_session):
    user = User('Martin', '123456789')
    user2 = User('Martin2', '123456789')

    insert_user(empty_session, user)
    insert_user(empty_session, user2)

    game = Game(1, 'Cool game')
    game2 = Game(2, 'Cool game2')

    insert_game(empty_session, game)
    insert_game(empty_session, game2)

    review = Review(user, game, 5, "Cool game")
    review2 = Review(user2, game2, 4, "Cool game2")

    insert_review(empty_session, review)
    insert_review(empty_session, review2)

    expected = [review, review2]
    result = empty_session.query(Review).all()

    for review in expected:
        assert review in result  # make sure all the reviews were added

    with pytest.raises(IntegrityError):
        insert_review(empty_session, review) # Try adding a review with the same user_id, game_id, rating and comment

def test_add_retrieve_wish(empty_session):
    game = Game(1, 'Cool game')
    game2 = Game(2, 'Cool game2')

    insert_game(empty_session, game)
    insert_game(empty_session, game2)

    user = User('Martin', '123456789')
    user2 = User('Martin2', '123456789')

    insert_user(empty_session, user)
    insert_user(empty_session, user2)

    wish = Wish(user, game)
    wish2 = Wish(user, game2)
    wish3 = Wish(user2, game)
    wish4 = Wish(user2, game2)

    insert_wish(empty_session, wish)
    insert_wish(empty_session, wish2)
    insert_wish(empty_session, wish3)
    insert_wish(empty_session, wish4)

    expected = [wish, wish2, wish3, wish4]

    result = empty_session.query(Wish).all()

    for wish in expected:
        assert wish in result # make sure all the reviews were added

    with pytest.raises(IntegrityError): # try adding an already existing review
        insert_wish(empty_session, wish)